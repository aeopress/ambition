#!/usr/bin/env bash
# evals/run.sh — 行為驗收契約（evals.json）自動化回歸
#
# 用法：
#   ./evals/run.sh                              # 跑全部案例，每案例預設跑 2 次
#   ./evals/run.sh --case 2                     # 只跑指定 id
#   ./evals/run.sh --runs 3                     # 每案例跑 3 次
#   ./evals/run.sh --rejudge <output.md> --case 3   # 只重跑 judge：用案例目前的 expectations 判定存檔輸出
#   EVAL_MODEL=claude-sonnet-5 ./evals/run.sh   # 指定模型（受測與 judge 同款；預設用 CLI 預設模型）
#   SKILL_FILE=/tmp/skill-v0.1.0.md ./evals/run.sh   # A/B：指定其他版本的 SKILL.md
#     （舊版取法：git show <commit>:skills/ambition/SKILL.md > /tmp/skill-v0.1.0.md）
#
# 每個案例每次執行兩段：
#   1. 受測：claude -p 以 SKILL.md 全文為附加 system prompt，執行 eval prompt
#   2. 判定：第二個 claude -p 擔任 judge，逐項核對 expectations，輸出 JSON
# 閘門（2026-10-19 起，統計式）：LLM judge 不是確定性的，同一案例同一 SKILL.md 會輪流倒不同的
# 字面條件。所以每案例跑 N 次（--runs，預設 2）：
#   - gate=any（預設）：N 次裡至少一次全過就算過。
#   - gate=all（案例自己在 evals.json 標 "gate": "all"，例如負向案例）：N 次都要全過。
# 產物存 evals/results/<時間戳>/case-<id>-r<n>-*（已列入 .gitignore）。任何案例未過則 exit 1。
#
# 隔離（2026-10-20 起）：受測與 judge 的 claude -p 都加 --setting-sources ""、--strict-mcp-config、
# --no-session-persistence，不載入使用者的 CLAUDE.md、權限設定與 MCP（實測：不加時受測會稱呼使用者暱稱、
# 照個人規則加「你要做什麼」段落，還會用權限放行的 Bash）。受測只給 --tools "WebSearch,WebFetch,Read"；
# 每次受測在臨時工作目錄執行，只放 skill/SKILL.md 與 skill/references/，結束後刪除。
# judge 用 --system-prompt 取代預設 system prompt 並關掉所有工具（只關工具而保留預設 prompt，
# 實測會把工具呼叫寫成純文字）。
# 受測異常：evals/check_output.py 判定空輸出、殘缺片段、推理外洩或把工具呼叫寫成純文字時，
# 該份改存成 *.anomaly-<n>.*、不交給 judge，重跑受測，最多 3 次。judge 輸出無法解析（含 API Error）時重試，最多 3 次。
#
# 限制：headless 模式沒有 AskUserQuestion；SKILL.md 第 1 步「兩軸都合適時問使用者」
# 分支不會觸發，evals 的 prompt 均設計為單一軸線明確。

set -euo pipefail

cd "$(dirname "$0")/.."
SKILL_FILE="${SKILL_FILE:-skills/ambition/SKILL.md}"
EVALS_FILE="${EVALS_FILE:-$PWD/evals/evals.json}"
RESULTS_DIR="$PWD/evals/results/$(date +%Y%m%d-%H%M%S)"
RUNS=2

CASE_FILTER=""
REJUDGE_FILE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --case) CASE_FILTER="$2"; shift 2 ;;
    --runs) RUNS="$2"; shift 2 ;;
    --rejudge) REJUDGE_FILE="$2"; shift 2 ;;
    *) echo "未知參數：$1（支援 --case <id>、--runs <n>、--rejudge <output.md>）" >&2; exit 2 ;;
  esac
done

command -v claude >/dev/null || { echo "找不到 claude CLI" >&2; exit 1; }
command -v jq >/dev/null || { echo "找不到 jq" >&2; exit 1; }

if [[ -n "$REJUDGE_FILE" ]]; then
  # 重判常平行跑，秒級時間戳會撞名；mktemp 加隨機尾碼，每次一個獨立目錄。
  mkdir -p evals/results
  RESULTS_DIR="$(mktemp -d "${RESULTS_DIR}-rejudge-XXXXXX")"
else
  mkdir -p "$RESULTS_DIR"
fi
SKILL_BODY="$(cat "$SKILL_FILE")"

# macOS 內建 bash 3.2 在 set -u 下展開空陣列會報錯，用條件展開保護
MODEL_ARGS=()
[[ -n "${EVAL_MODEL:-}" ]] && MODEL_ARGS=(--model "$EVAL_MODEL")
ISOLATION_ARGS=(--setting-sources "" --strict-mcp-config --no-session-persistence)
JUDGE_SYSTEM="你是行為驗收的 judge。只輸出使用者要求的 JSON。你沒有任何工具，也不需要工具。"

# judge：用案例的 prompt 與 expectations 判定一份輸出檔，結果寫進 judge 檔。
# 參數：<prompt> <expectations> <輸出檔> <judge 檔> <stderr 檔>
judge() {
  local prompt="$1" expectations="$2" out_file="$3" judge_file="$4" stderr_file="$5"
  local judge_prompt="你是行為驗收的 judge。以下是一個 skill 對測試 prompt 的實際輸出，以及逐項驗收條件。
請逐項判定 pass/fail，嚴格依字面條件核對，不要腦補輸出中不存在的內容。
只輸出 JSON（不要 code fence、不要任何其他文字），格式：
{\"results\":[{\"n\":1,\"pass\":true,\"reason\":\"一句話\"}],\"overall_pass\":true}
overall_pass 為所有項目皆 pass 才是 true。

## 測試 prompt
$prompt

## 驗收條件
$expectations

## 實際輸出（主對話完整逐字稿）
$(cat "$out_file")"

  # judge 的 claude -p 實測會在完整輸出 JSON 之後仍以非零碼結束，stderr 印
  # 「No messages returned from query」（2026-10-17，連續三次）。輸出檔是完整的，
  # 所以不讓 pipefail 中止整支腳本，一律以 judge 檔能否解析為準。
  # 輸出無法解析成 {"results": [...]}（含 API Error、空輸出）時重試，最多 3 次。
  local attempt
  for attempt in 1 2 3; do
    set +e
    claude -p "$judge_prompt" --system-prompt "$JUDGE_SYSTEM" --tools "" "${ISOLATION_ARGS[@]}" \
      ${MODEL_ARGS[@]+"${MODEL_ARGS[@]}"} 2>"$stderr_file" \
      | sed -e '/^```/d' > "$judge_file"
    set -e
    jq -e '.results | type == "array"' "$judge_file" >/dev/null 2>&1 && return 0
    [[ "$attempt" -lt 3 ]] && echo "   （judge 第 ${attempt} 次輸出無法解析，重試：$(head -c 80 "$judge_file" | tr '\n' ' ')）"
  done
  return 0
}

# 列出未過項目；judge 檔無法解析時印原文。
print_failures() {
  jq -r '.results[] | select(.pass == false) | "   - 條件 \(.n)：\(.reason)"' "$1" 2>/dev/null \
    || { echo "   （judge 輸出無法解析，原文如下）"; cat "$1"; }
}

case_field() {
  jq -r ".evals[] | select(.id==$1) | $2" "$EVALS_FILE"
}

case_expectations() {
  jq -r ".evals[] | select(.id==$1) | .expectations | to_entries | map(\"\\(.key + 1). \\(.value)\") | join(\"\\n\")" "$EVALS_FILE"
}

# 重判模式：不跑受測，只用目前的 expectations 判定存檔輸出。
if [[ -n "$REJUDGE_FILE" ]]; then
  [[ -n "$CASE_FILTER" ]] || { echo "--rejudge 需要搭配 --case <id>" >&2; exit 2; }
  [[ -f "$REJUDGE_FILE" ]] || { echo "找不到輸出檔：$REJUDGE_FILE" >&2; exit 2; }
  judge "$(case_field "$CASE_FILTER" .prompt)" "$(case_expectations "$CASE_FILTER")" "$REJUDGE_FILE" \
    "$RESULTS_DIR/rejudge-case-$CASE_FILTER-judge.json" "$RESULTS_DIR/rejudge-case-$CASE_FILTER-judge.stderr"
  if jq -e '.overall_pass == true' "$RESULTS_DIR/rejudge-case-$CASE_FILTER-judge.json" >/dev/null 2>&1; then
    echo "== rejudge case ${CASE_FILTER}：PASS（判定：$RESULTS_DIR/rejudge-case-$CASE_FILTER-judge.json）"
    exit 0
  fi
  echo "== rejudge case ${CASE_FILTER}：FAIL（判定：$RESULTS_DIR/rejudge-case-$CASE_FILTER-judge.json）"
  print_failures "$RESULTS_DIR/rejudge-case-$CASE_FILTER-judge.json" | sed -e 's/^   //'
  exit 1
fi

total=0
passed=0
failed=0

for id in $(jq -r '.evals[].id' "$EVALS_FILE"); do
  if [[ -n "$CASE_FILTER" && "$id" != "$CASE_FILTER" ]]; then
    continue
  fi
  total=$((total + 1))
  title=$(case_field "$id" .title)
  prompt=$(case_field "$id" .prompt)
  gate=$(case_field "$id" '.gate // "any"')
  expectations=$(case_expectations "$id")

  echo "== case ${id}：${title}"
  run_passes=0
  for ((r = 1; r <= RUNS; r++)); do
    raw_file="$RESULTS_DIR/case-$id-r$r-raw.jsonl"
    out_file="$RESULTS_DIR/case-$id-r$r-output.md"
    judge_file="$RESULTS_DIR/case-$id-r$r-judge.json"
    # stream-json 抓完整逐字稿：軸線點名等中間訊息可能不在最終回覆裡，只抓最後一則會漏。
    # 只給 WebSearch、WebFetch、Read：Read 讀取工作目錄內的 skill 與 references；不做 subagent 編排，也不能真的叫到本機安裝的
    # best-minds plugin（2026-10-19 實測，案例 4 的受測呼叫了 best-minds，開圓桌、查網路、還把辯論寫進 docs.local）。
    # perl alarm 硬逾時 15 分鐘＋自動重試：headless 偶發 API 端卡死（tool_result 已回、
    # 下一個 assistant 訊息永不到）。逾時（exit 142）自動重試最多三次，其他錯誤直接失敗。
    attempt=1
    anomaly_try=1
    anomaly=""
    while :; do
      ws="$(mktemp -d "${TMPDIR:-/tmp}/ambition-eval-XXXXXX")"
      mkdir -p "$ws/skill"
      cp "$SKILL_FILE" "$ws/skill/SKILL.md"
      cp -R skills/ambition/references "$ws/skill/references"
      skill_prompt="Base directory for this skill: $ws/skill
$SKILL_BODY"
      set +e
      ( cd "$ws" &&
      CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=900000 \
      perl -e 'alarm shift @ARGV; exec @ARGV' 900 claude -p "$prompt" \
        --append-system-prompt "$skill_prompt" \
        --tools "WebSearch,WebFetch,Read" \
        --allowedTools "WebSearch,WebFetch,Read" \
        "${ISOLATION_ARGS[@]}" \
        --output-format stream-json --verbose \
        ${MODEL_ARGS[@]+"${MODEL_ARGS[@]}"} ) > "$raw_file"
      subject_rc=$?
      rm -rf "$ws"
      set -e
      if [[ "$subject_rc" -ne 0 ]]; then
        if [[ "$subject_rc" -eq 142 && "$attempt" -lt 3 ]]; then
          echo "   （run ${r} 受測第 ${attempt} 次逾時——API 卡死樣態，自動重試）"
          attempt=$((attempt + 1))
          continue
        fi
        echo "   受測執行失敗（exit ${subject_rc}）" >&2
        exit 1
      fi
      jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "text") | .text' \
        "$raw_file" > "$out_file"
      anomaly="$(python3 -I evals/check_output.py "$out_file" "$prompt" || true)"
      [[ -z "$anomaly" ]] && break
      mv "$raw_file" "${raw_file%.jsonl}.anomaly-${anomaly_try}.jsonl"
      mv "$out_file" "${out_file%.md}.anomaly-${anomaly_try}.md"
      echo "   （run ${r} 受測第 ${anomaly_try} 次輸出異常：${anomaly}；不交給 judge）"
      [[ "$anomaly_try" -ge 3 ]] && break
      anomaly_try=$((anomaly_try + 1))
    done

    if [[ -n "$anomaly" ]]; then
      echo "   run ${r}：FAIL — 受測連續 3 次輸出異常，未判定"
      continue
    fi

    judge "$prompt" "$expectations" "$out_file" "$judge_file" "$RESULTS_DIR/case-$id-r$r-judge.stderr"

    if jq -e '.overall_pass == true' "$judge_file" >/dev/null 2>&1; then
      run_passes=$((run_passes + 1))
      echo "   run ${r}：PASS（輸出：${out_file}）"
    else
      echo "   run ${r}：FAIL — 未過項目："
      print_failures "$judge_file"
      echo "   （輸出：${out_file}；判定：${judge_file}）"
    fi
  done

  if { [[ "$gate" == "all" ]] && [[ "$run_passes" -eq "$RUNS" ]]; } || { [[ "$gate" != "all" ]] && [[ "$run_passes" -ge 1 ]]; }; then
    passed=$((passed + 1))
    echo "   PASS（${run_passes}/${RUNS} 次全過，gate=${gate}）"
  else
    failed=$((failed + 1))
    echo "   FAIL（${run_passes}/${RUNS} 次全過，gate=${gate}）"
  fi
done

echo ""
echo "== 總結：$passed/$total 過（每案例 ${RUNS} 次），產物在 $RESULTS_DIR"
[[ "$failed" -eq 0 ]]
