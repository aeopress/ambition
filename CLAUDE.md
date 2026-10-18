# CLAUDE.md

## 專案概述

Claude Code 與 Codex CLI 雙平台 skill，把一個任務「做深、不做大」。方法來自 Felix Rieseberg 2026-10-13 的文章。三軸：Altitude（任務背後的結果）、Depth（頂尖從業者的材料、方法與外部裁判）、Range（其他領域的工具）。Speed 不處理，文章明寫它不需要技巧。

交付物固定：點名軸線、依軸分析、一段 fenced prompt、停下。

**語言策略**：`skills/ambition/SKILL.md` 正本以英文撰寫，STE 風格（短句、主動語態、一物一名），開頭明令跟隨使用者語言。`README.md` 是正體中文主說明，`README_en.md` 是英文版。

## 專案結構

```
ambition/
├── .claude-plugin/
│   ├── marketplace.json          # Claude Code marketplace 清單（source: "./"）
│   └── plugin.json               # Claude Code plugin 清單
├── skills/ambition/SKILL.md      # 唯一正本
├── .agents/plugins/marketplace.json   # Codex marketplace 清單（指向 ./plugins/ambition）
├── plugins/ambition/
│   ├── .codex-plugin/plugin.json # Codex plugin 清單
│   └── skills/ambition/
│       ├── SKILL.md              # Codex 平台變體（只有平台機制不同）
│       └── agents/openai.yaml    # Codex 選單中繼資料
├── SKILL.md                      # → skills/ambition/SKILL.md 的 symlink
├── evals/evals.json              # 行為驗收契約，一軸一案
├── evals/run.sh                  # 自動回歸
├── .claude/plans/                # 計畫檔，有追蹤
├── README.md                     # 正體中文主說明
├── README_en.md                  # 英文版
└── LICENSE                       # MIT
```

## 修改須知

修改 `skills/ambition/SKILL.md` 時，須同步：

1. 檔頭 YAML frontmatter 與 HTML 註解。
2. `.claude-plugin/marketplace.json`、`.claude-plugin/plugin.json`、`plugins/ambition/.codex-plugin/plugin.json` 的 version，三處相等。
3. 方法論變動移植到 `plugins/ambition/skills/ambition/SKILL.md`。該檔只在平台機制上不同：frontmatter 只留 name 與 description、一般提問取代 AskUserQuestion、「使用 best-minds skill」取代 Skill tool 呼叫。
4. 方法論變動同步 `README.md`（正體中文）與 `README_en.md`（英文）。
5. 改護欄後對照 `evals/evals.json`，可跑 `evals/run.sh`；`--case 2` 最便宜。

根目錄 `SKILL.md` 是 symlink，不要直接編輯或以實體檔案覆蓋。

## 寫作原則

- 依 mattpocock `writing-for-agents`：leading word 當 token 用（Altitude、Depth、Range、deeper not bigger、outside judge），每步有完成判準，正面陳述目標行為，護欄才用禁止句並配上正面目標。
- 技巧轉述，不抄文章原文。只逐字引用 Depth 那段四題 prompt 並標出處。
- 與 best-minds 的分界寫在 SKILL.md 的「Relation to best-minds」，兩邊改動要互相對照。
