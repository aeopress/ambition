# ambition

Claude Code 與 Codex CLI 的 skill。給它一個任務，它把任務做深、不做大，改寫成一段 prompt，然後停下。

方法來自 Felix Rieseberg 的 [How to be more ambitious: A tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/)（2026-10-13）。Depth 的四題逐字引用他的 prompt。結構參考 [DannyMac180/skills 的 be-ambitious](https://github.com/DannyMac180/skills/tree/main/be-ambitious)（MIT）。

## 它做什麼

1. **分流軸線。** Altitude：任務是結果的代理。Depth：任務要做到頂尖從業者的水準。Range：其他領域有更好的工具。Speed：照原樣執行，不需要技巧。
2. **依軸線分析。** Altitude 寫出目標背後的目標、三階梯與前置條件。Depth 回答四題：從業者會多做什麼、最原始的材料、具名的方法與工具、外部裁判。Range 先把名詞換成動詞，再依工具列出領域。
3. **改寫並停下。** 一段 fenced prompt，用你的口吻，以外部檢查收尾。skill 提議執行，然後等你。

回覆語言跟隨任務語言。分析段用短句、主動語態、一物一名。

## 與 best-minds 的關係

[best-minds](https://github.com/yelban/best-minds.TW) 替判斷題召集真實人物的觀點。`ambition` 把一個方向改成能以專業水準執行的 prompt。Range 替要執行的任務找領域與工具，best-minds 替決策找觀點。

## 安裝

Claude Code：

```text
/plugin marketplace add yelban/ambition.TW
/plugin install ambition@ambition
```

Codex CLI：

```text
codex plugin marketplace add .
codex plugin add ambition@ambition
```

## 例子

```text
/ambition 幫我照模板把這季資料做成 QBR 簡報
/ambition 我們相信流失是 onboarding 的問題，幫我寫分析
/ambition 要讓主管 30 分鐘內決定預算，哪些領域的方法能借來用
```

## Evals

`evals/evals.json` 有三個案例，一軸一案。`./evals/run.sh` 跑全部，`./evals/run.sh --case 2` 跑一個。

## 授權

MIT
