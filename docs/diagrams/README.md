# Diagrams

The flowchart in both READMEs. Drawn with [diagram-design](https://github.com/cathrynlavery/diagram-design) (flowchart type, default editorial skin).

| File | Used by |
|---|---|
| `ambition-flow.svg`, `ambition-flow-dark.svg` | `README.md` (English, Geist) |
| `ambition-flow-zh-TW-hand.svg`, `ambition-flow-zh-TW-hand-dark.svg` | `README_zh-TW.md` (正體中文, 清松手寫體 2) |
| `ambition-flow*.html` | The sources the SVGs are exported from |
| `gen_flow.py` | Writes every HTML source from one layout and two label sets |

The SVGs embed subsets of their fonts as base64, because a GitHub README shows an SVG through `<img>` and that cannot load web fonts. The HTML sources do not embed anything: the English ones load Geist from Google Fonts, the handwriting ones use the locally installed JasonHandwriting2.

## Fonts

All three are under the SIL Open Font License 1.1. The license texts are in `fonts/`.

- `fonts/geist-subset.woff2`, `fonts/geistmono-subset.woff2`: Geist and Geist Mono by Vercel, no reserved name, so the subsets keep their family names.
- `fonts/jh2-subset.woff2`: 清松手寫體 2 (JasonHandwriting2) by Jason (Yu Ching Sung). Its OFL reserves the name JasonHandwriting2, so this subset is renamed `JH2 Subset`.

Each subset holds only the characters the diagram uses.

## Regenerate

Needs `uv`, Python 3, JasonHandwriting2 installed in `~/Library/Fonts/`, and the two Geist variable fonts in `fonts/src/` (download `Geist[wght].ttf` and `GeistMono[wght].ttf` from `google/fonts` under `ofl/geist` and `ofl/geistmono`, plus their `OFL.txt` as `geist-OFL.txt` and `geistmono-OFL.txt`). Then, from this directory:

```bash
uv run --no-project --with fonttools --with brotli python -I gen_flow.py --hand
python3 <diagram-design>/skills/diagram-design/scripts/export_svg.py ambition-flow.html ambition-flow.svg   # and the other three
uv run --no-project --with fonttools python -I gen_flow.py --inject ambition-flow.svg ambition-flow-dark.svg ambition-flow-zh-TW-hand.svg ambition-flow-zh-TW-hand-dark.svg
```

Check the sources with diagram-design's `scripts/self_check.py` before exporting.
