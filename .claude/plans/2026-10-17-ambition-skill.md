# ambition skill 計畫（2026-10-17）

## 決策（已與吹吹確認，Q1 到 Q7 全採建議）

1. **只做三軸加分流。** 來源文章明寫 Speed 不需要技巧，所以 skill 開頭先分流：Altitude、Depth、Range 三軸之一，或判定「只需要 Speed，照原樣執行」。不替 Speed 發明方法。
2. **一個 skill，內建分流，不拆三個。** 三軸共用同一種交付物，拆開會重複。
3. **model-invoked。** description 一分支一個觸發詞。這樣 best-minds 收斂後可以用 Skill tool 呼叫它。
4. **交付物統一。** 三軸都以「改寫後的 prompt 放單一 fenced block，然後停下、一句話問要不要跑」收尾。各軸有自己的前置分析：Altitude 給目標階梯與前置條件；Depth 照 Felix 四題；Range 先名詞換動詞，再列領域與工具。
5. **輸出套八成 STE。** 分析段短句、主動語態、一物一名，不限語言。改寫後的 prompt 用使用者口吻，不套。
6. **與 best-minds 的分界寫進兩邊。** Range 給可執行任務找領域與工具；best-minds 給判斷題找觀點。本次只寫進 ambition 這邊，best-minds 那邊列為後續。
7. **佈局照 best-minds.TW。** 英文正本、跟隨使用者語言、Codex 雙平台（`.agents/plugins/marketplace.json` 是正門）、`evals/` 三案例。
8. **Meta Vocabulary 採 writing-for-agents 那套。** leading word、context pointer、completion criterion、progressive disclosure、positive phrasing。

## 來源與授權

- Felix Rieseberg，《How to be more ambitious: A tutorial for humans with models》，2026-10-13。技巧轉述，只逐字引用 Depth 那段四題 prompt並標出處。
- DannyMac180/skills 的 be-ambitious（MIT）。參考其結構：輸入規則、四題、改寫後停下。
- Karpathy 2026-10-02 推文：要求模型輸出用 ASD-STE100 較好讀，取八成。

## 檔案

- `skills/ambition/SKILL.md`：唯一正本。
- `SKILL.md`：symlink 到正本，舊式安裝相容。
- `.claude-plugin/marketplace.json`、`.claude-plugin/plugin.json`：Claude Code 清單。
- `.agents/plugins/marketplace.json`、`plugins/ambition/.codex-plugin/plugin.json`：Codex 清單。
- `plugins/ambition/skills/ambition/SKILL.md`：Codex 平台變體。差異只有：frontmatter 只留 name 與 description、AskUserQuestion 改成一般提問、Skill tool 呼叫改成「使用 best-minds skill」。
- `plugins/ambition/skills/ambition/agents/openai.yaml`：Codex 選單中繼資料。
- `evals/evals.json`：三案例，一軸一案，用文章自己的 QBR 與 churn 例子。
- `evals/run.sh`：從 best-minds.TW 複製改名。
- `README.md`、`README_zh-TW.md`、`CLAUDE.md`、`LICENSE`、`.gitignore`。

## 版本

0.1.0。三處 version 要相等。

## 未解決

- best-minds 那邊的分界條款與「收斂後呼叫 ambition」尚未寫入，要另開 best-minds.TW 的修訂。
- 第四個 eval 案例（判斷題應轉交 best-minds 的負向案例）尚未寫。
- 三個案例尚未實跑。跑法：`./evals/run.sh --case 2` 最便宜。
- Codex 端尚未實裝驗證（`codex plugin marketplace add .` 後 diff cache 裡的 SKILL.md）。
