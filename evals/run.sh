#!/usr/bin/env bash
# evals/run.sh — 行為驗收契約（evals.json）自動化回歸
#
# 用法：
#   ./evals/run.sh                              # 跑全部案例
#   ./evals/run.sh --case 2                     # 只跑指定 id
#   EVAL_MODEL=claude-sonnet-5 ./evals/run.sh   # 指定模型（受測與 judge 同款；預設用 CLI 預設模型）
#   SKILL_FILE=/tmp/skill-v0.1.0.md ./evals/run.sh   # A/B：指定其他版本的 SKILL.md
#     （舊版取法：git show <commit>:skills/ambition/SKILL.md > /tmp/skill-v0.1.0.md）
#
# 每個案例兩段：
#   1. 受測：claude -p 以 SKILL.md 全文為附加 system prompt，執行 eval prompt
#   2. 判定：第二個 claude -p 擔任 judge，逐項核對 expectations，輸出 JSON
# 產物存 evals/results/<時間戳>/（已列入 .gitignore）。任何案例未全過則 exit 1。
#
# 限制：headless 模式沒有 AskUserQuestion；SKILL.md 第 1 步「兩軸都合適時問使用者」
# 分支不會觸發，evals 的 prompt 均設計為單一軸線明確。
# 從 best-minds.TW 的 evals/run.sh 複製改名，逾時與重試邏輯沿用。

set -euo pipefail

cd "$(dirname "$0")/.."
SKILL_FILE="${SKILL_FILE:-skills/ambition/SKILL.md}"
EVALS_FILE="evals/evals.json"
RESULTS_DIR="evals/results/$(date +%Y%m%d-%H%M%S)"

CASE_FILTER=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --case) CASE_FILTER="$2"; shift 2 ;;
    *) echo "未知參數：$1（支援 --case <id>）" >&2; exit 2 ;;
  esac
done

command -v claude >/dev/null || { echo "找不到 claude CLI" >&2; exit 1; }
command -v jq >/dev/null || { echo "找不到 jq" >&2; exit 1; }

mkdir -p "$RESULTS_DIR"
SKILL_BODY="$(cat "$SKILL_FILE")"

# macOS 內建 bash 3.2 在 set -u 下展開空陣列會報錯，用條件展開保護
MODEL_ARGS=()
[[ -n "${EVAL_MODEL:-}" ]] && MODEL_ARGS=(--model "$EVAL_MODEL")

total=0
passed=0
failed=0

for id in $(jq -r '.evals[].id' "$EVALS_FILE"); do
  if [[ -n "$CASE_FILTER" && "$id" != "$CASE_FILTER" ]]; then
    continue
  fi
  total=$((total + 1))
  title=$(jq -r ".evals[] | select(.id==$id) | .title" "$EVALS_FILE")
  prompt=$(jq -r ".evals[] | select(.id==$id) | .prompt" "$EVALS_FILE")
  expectations=$(jq -r ".evals[] | select(.id==$id) | .expectations | to_entries | map(\"\(.key + 1). \(.value)\") | join(\"\n\")" "$EVALS_FILE")

  echo "== case ${id}：${title}"
  raw_file="$RESULTS_DIR/case-$id-raw.jsonl"
  out_file="$RESULTS_DIR/case-$id-output.md"
  # stream-json 抓完整逐字稿：軸線點名等中間訊息可能不在最終回覆裡，只抓最後一則會漏。
  # 停用 Agent/Task：evals 驗的是輸出契約，不是 subagent 編排。
  # 停用 Skill：受測只能用文字說明轉交，不能真的叫到本機安裝的 best-minds plugin
  # （2026-10-19 實測，案例 4 的受測呼叫了 best-minds，開圓桌、查網路、還把辯論寫進 docs.local）。
  # perl alarm 硬逾時 15 分鐘＋自動重試：headless 偶發 API 端卡死（tool_result 已回、
  # 下一個 assistant 訊息永不到）。逾時（exit 142）自動重試最多三次，其他錯誤直接失敗。
  attempt=1
  while :; do
    set +e
    CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=900000 \
    perl -e 'alarm shift @ARGV; exec @ARGV' 900 claude -p "$prompt" \
      --append-system-prompt "$SKILL_BODY" \
      --allowedTools "WebSearch,WebFetch" \
      --disallowedTools "Agent,Task,Skill" \
      --output-format stream-json --verbose \
      ${MODEL_ARGS[@]+"${MODEL_ARGS[@]}"} > "$raw_file"
    subject_rc=$?
    set -e
    [[ "$subject_rc" -eq 0 ]] && break
    if [[ "$subject_rc" -eq 142 && "$attempt" -lt 3 ]]; then
      echo "   （受測第 ${attempt} 次逾時——API 卡死樣態，自動重試）"
      attempt=$((attempt + 1))
      continue
    fi
    echo "   受測執行失敗（exit ${subject_rc}）" >&2
    exit 1
  done
  jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "text") | .text' \
    "$raw_file" > "$out_file"

  judge_prompt="你是行為驗收的 judge。以下是一個 skill 對測試 prompt 的實際輸出，以及逐項驗收條件。
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

  judge_file="$RESULTS_DIR/case-$id-judge.json"
  # judge 的 claude -p 實測會在完整輸出 JSON 之後仍以非零碼結束，stderr 印
  # 「No messages returned from query」（2026-10-17，連續三次）。輸出檔是完整的，
  # 所以不讓 pipefail 中止整支腳本，一律以 judge 檔能否解析為準。
  set +e
  claude -p "$judge_prompt" ${MODEL_ARGS[@]+"${MODEL_ARGS[@]}"} 2>"$RESULTS_DIR/case-$id-judge.stderr" \
    | sed -e '/^```/d' > "$judge_file"
  set -e

  if jq -e '.overall_pass == true' "$judge_file" >/dev/null 2>&1; then
    passed=$((passed + 1))
    echo "   PASS（輸出：${out_file}）"
  else
    failed=$((failed + 1))
    echo "   FAIL — 未過項目："
    jq -r '.results[] | select(.pass == false) | "   - 條件 \(.n)：\(.reason)"' "$judge_file" 2>/dev/null \
      || { echo "   （judge 輸出無法解析，原文如下）"; cat "$judge_file"; }
    echo "   （輸出：${out_file}；判定：${judge_file}）"
  fi
done

echo ""
echo "== 總結：$passed/$total 過，產物在 $RESULTS_DIR"
[[ "$failed" -eq 0 ]]
