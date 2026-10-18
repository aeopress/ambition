#!/usr/bin/env python3
"""Generate the ambition flowchart in four variants (en/zh-TW x light/dark).

Layout follows diagram-design's flowchart conventions: shape carries type,
top-down flow, every branch labelled, coral on the end node and its arrow only.
Output: ambition-flow[-zh-TW][-dark].html next to this script.

Optional: `--hand` also writes ambition-flow-zh-TW-hand[-dark].html, a zh-TW
variant set entirely in a subset of JasonHandwriting2 (OFL 1.1), embedded as a
base64 @font-face so the SVG renders the same inside a GitHub README <img>.
Run that mode with: uv run --no-project --with fonttools --with brotli python -I gen_flow.py --hand
"""
import base64
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT_SRC = Path.home() / "Library/Fonts/JasonHandwriting2-Regular.ttf"
SUBSET_FAMILY = "JH2 Subset"  # OFL reserved font name must not be reused on a modified (subset) font

PALETTE = {
    "light": dict(paper="#f5f5f5", ink="#2d3142", muted="#4f5d75", accent="#bf4520",
                  node="#ffffff", dots="rgba(45,49,66,0.10)", oval="rgba(45,49,66,0.03)",
                  oval_stroke="rgba(45,49,66,0.30)", tint="rgba(191,69,32,0.08)",
                  rule="rgba(45,49,66,0.10)"),
    "dark": dict(paper="#2d3142", ink="#f5f5f5", muted="#bfc0c0", accent="#f08a59",
                 node="#393e53", dots="rgba(245,245,245,0.10)", oval="rgba(245,245,245,0.03)",
                 oval_stroke="rgba(245,245,245,0.30)", tint="rgba(240,138,89,0.08)",
                 rule="rgba(245,245,245,0.10)"),
}

FONT_LINK = {
    "en": "https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap",
    "zh": "https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;600&family=Noto+Serif+TC:wght@400&display=swap",
}
FONTS = {
    "en": dict(sans="'Geist', sans-serif", mono="'Geist Mono', monospace",
               serif="'Instrument Serif', serif", lang="en"),
    "zh": dict(sans="'Geist', 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif",
               mono="'Geist Mono', 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', monospace",
               serif="'Instrument Serif', 'Noto Serif TC', serif", lang="zh-Hant-TW"),
}
HAND_STACK = f"'{SUBSET_FAMILY}', 'JasonHandwriting2', 'Noto Sans TC', 'PingFang TC', sans-serif"

# Type sizes per role. The handwriting face is thin, so it gets a larger ramp.
SIZES = {
    "default": dict(name=12, desc=10, sub=9, label=8, legend=8.5, ltitle=8, mask_h=12),
    "hand": dict(name=15, desc=13, sub=12, label=11, legend=11, ltitle=10, mask_h=16),
}

TEXT = {
    "en": dict(
        eyebrow="Flowchart · ambition",
        h1="What ambition does with a task",
        title="What ambition does with a task",
        desc="Flowchart of how the ambition skill routes a task: Speed runs it as asked, a judgment call goes to best-minds, and a higher bar picks Altitude, Depth or Range before one rewritten prompt with an outside check.",
        start="A task you're about to hand the AI",
        d1=("What does", "it need?"),
        speed=("Speed", "run it as asked"),
        bm=("best-minds round table", "no single right answer"),
        d2="Which axis?",
        alt=("Altitude", "The outcome behind the task.", "Ladder up, list what it needs first."),
        dep=("Depth", "What a top professional does:", "raw material, named tools, outside judge"),
        rng=("Range", "Nouns to verbs, then borrow", "instruments from other fields."),
        end=("One rewritten prompt,", "ending with an outside check", "then it stops, you decide whether to run it"),
        lbl=dict(just="JUST DONE", dec="A DECISION", bar="A HIGHER BAR", alt="ALTITUDE", dep="DEPTH", rng="RANGE"),
        legend_title="LEGEND · SHAPE CARRIES TYPE",
        legend=("Start / end (oval)", "Step (rectangle)", "Decision (diamond)", "Merge", "Happy path", "Branch", "Hand-off"),
    ),
    "zh": dict(
        eyebrow="流程圖 · ambition",
        h1="ambition 怎麼處理一個任務",
        title="ambition 怎麼處理一個任務",
        desc="流程圖：ambition 如何分流一個任務。只要做完就照原樣執行（Speed），判斷題交給 best-minds，要更高標準則選 Altitude、Depth 或 Range，最後產出一段以外部檢查收尾的改寫 prompt。",
        start="你準備交給 AI 的任務",
        d1=("這個任務", "需要什麼？"),
        speed=("Speed", "照原樣執行"),
        bm=("best-minds 圓桌", "沒有標準答案的判斷題"),
        d2="走哪一軸？",
        alt=("Altitude", "任務背後的結果。", "往上拉階梯，先列出模型需要什麼。"),
        dep=("Depth", "頂尖從業者怎麼做：", "最原始的材料、具名工具、外部裁判。"),
        rng=("Range", "先把名詞換成動詞，", "再向其他領域借工具。"),
        end=("一段改寫後的 prompt，", "以外部檢查收尾。", "然後停下，由你決定要不要跑。"),
        lbl=dict(just="只要做完", dec="要做決定", bar="要更高標準", alt="ALTITUDE", dep="DEPTH", rng="RANGE"),
        legend_title="圖例 · 形狀代表類型",
        legend=("起點／終點（橢圓）", "步驟（矩形）", "決策（菱形）", "匯合", "主路徑", "分支", "交接（虛線）"),
    ),
}

LS = ' letter-spacing="0.12em"'


def all_chars(t: dict) -> str:
    out = set()
    for v in t.values():
        if isinstance(v, str):
            out.update(v)
        elif isinstance(v, dict):
            for s in v.values():
                out.update(s)
        else:
            for s in v:
                out.update(s)
    return "".join(sorted(out))


ASCII = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:;()/-'·"
FONTS_DIR = OUT / "fonts"


def subset_face(src: Path, out_name: str, chars: str, family: str, rename: str = "",
                weight_range: str = "100 900") -> str:
    """Subset a font to `chars`, save as fonts/<out_name>.woff2, return a base64 @font-face rule.

    `rename` sets a new family name in the name table (needed when the OFL reserves the
    original name, as JasonHandwriting2 does). Variable fonts keep their axes.
    """
    from fontTools import subset
    from fontTools.ttLib import TTFont

    FONTS_DIR.mkdir(exist_ok=True)
    woff = FONTS_DIR / f"{out_name}.woff2"
    font = TTFont(str(src))
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.name_IDs = ["*"]
    opts.name_legacy = True
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(font)
    if rename:
        for n in font["name"].names:
            if n.nameID in (1, 4, 16):
                n.string = rename
            elif n.nameID == 6:
                n.string = rename.replace(" ", "")
    font.flavor = "woff2"
    font.save(str(woff))
    b64 = base64.b64encode(woff.read_bytes()).decode("ascii")
    print(f"subset {out_name}: {len(chars)} chars -> {woff.stat().st_size} bytes woff2")
    return (f"@font-face {{ font-family: '{family}'; font-weight: {weight_range}; "
            f"src: url(data:font/woff2;base64,{b64}) format('woff2'); }}")


def hand_font_face() -> str:
    """JasonHandwriting2 (OFL 1.1, reserved name) -> renamed subset covering the zh-TW text."""
    from fontTools.ttLib import TTFont
    for n in TTFont(str(FONT_SRC))["name"].names:
        if n.nameID == 13 and n.platformID == 3:
            (FONTS_DIR / "JasonHandwriting2-OFL.txt").write_text(n.toUnicode(), encoding="utf-8")
    face = subset_face(FONT_SRC, "jh2-subset", all_chars(TEXT["zh"]) + ASCII,
                       SUBSET_FAMILY, rename=SUBSET_FAMILY, weight_range="400 600")
    (FONTS_DIR / "jh2-font-face.css").write_text(face, encoding="utf-8")
    return face


def geist_font_faces() -> str:
    """Geist + Geist Mono (OFL 1.1, no reserved name) -> subsets covering the English text."""
    import shutil
    src = FONTS_DIR / "src"
    chars = all_chars(TEXT["en"]) + ASCII
    faces = [
        subset_face(src / "Geist[wght].ttf", "geist-subset", chars, "Geist"),
        subset_face(src / "GeistMono[wght].ttf", "geistmono-subset", chars, "Geist Mono"),
    ]
    shutil.copy(src / "geist-OFL.txt", FONTS_DIR / "Geist-OFL.txt")
    shutil.copy(src / "geistmono-OFL.txt", FONTS_DIR / "GeistMono-OFL.txt")
    css = "\n".join(faces)
    (FONTS_DIR / "geist-font-face.css").write_text(css, encoding="utf-8")
    return css


def inject_faces(svg_path: Path) -> None:
    """Insert (or replace) the embedded @font-face style block right after </desc> in an exported SVG."""
    import re
    css_name = "jh2-font-face.css" if "-hand" in svg_path.name else "geist-font-face.css"
    face = (FONTS_DIR / css_name).read_text(encoding="utf-8")
    s = svg_path.read_text(encoding="utf-8")
    # A standalone SVG is parsed as XML, so the marker attribute must carry a value.
    s = re.sub(r"\n<style data-embedded-fonts[^>]*>.*?</style>", "", s, count=1, flags=re.S)
    i = s.index("</desc>") + len("</desc>")
    s = s[:i] + f'\n<style data-embedded-fonts="1">{face}</style>' + s[i:]
    svg_path.write_text(s, encoding="utf-8")
    print(f"injected {css_name} -> {svg_path.name} ({svg_path.stat().st_size} bytes)")


def label_width(s: str, size: float) -> int:
    """Mask width for a mono arrow label: wide chars cost 1.1em, narrow 0.72em, plus pad, snapped to 4."""
    w = sum(size * 1.1 if ord(c) > 0x2E7F else size * 0.72 for c in s) + 12
    return int(-(-w // 4) * 4)


def build(lang: str, theme: str, hand: bool = False, font_face: str = "") -> str:
    p, t = PALETTE[theme], TEXT[lang]
    f = dict(FONTS[lang])
    sz = SIZES["hand" if hand else "default"]
    if hand:
        f.update(sans=HAND_STACK, mono=HAND_STACK, serif=HAND_STACK)
    slug = "ambition-flow" + ("-zh-tw" if lang == "zh" else "") + ("-hand" if hand else "") + ("-dark" if theme == "dark" else "")
    sans, mono = f["sans"], f["mono"]
    m, ink, acc = p["muted"], p["ink"], p["accent"]

    def txt(x, y, s, size, weight=None, fill=None, family=None, anchor="middle", extra=""):
        fill = fill or ink
        family = family or sans
        w = f' font-weight="{weight}"' if weight else ""
        a = f' text-anchor="{anchor}"' if anchor else ""
        return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}"{w} font-family="{family}"{a}{extra}>{s}</text>'

    def arrow_label(cx, y_top, s, fill=None):
        w = label_width(s, sz["label"])
        h = sz["mask_h"]
        return (f'<rect x="{cx - w // 2}" y="{y_top}" width="{w}" height="{h}" rx="2" fill="{p["paper"]}"/>\n'
                f'        {txt(cx, y_top + h - 3, s, sz["label"], None, fill or m, mono, extra=LS)}')

    def beside(x_line, y_top, s):
        """Label beside a vertical segment: mask starts 8px right of the line."""
        w = label_width(s, sz["label"])
        return arrow_label(x_line + 8 + w // 2, y_top, s)

    def oval(x, y, w, h, fill=None, stroke=None):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill or p["oval"]}" stroke="{stroke or p["oval_stroke"]}" stroke-width="1"/>'

    def box(x, y, w, h):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{p["node"]}" stroke="{ink}" stroke-width="1"/>'

    def diamond(cx, top):
        return f'<polygon points="{cx},{top} {cx + 100},{top + 52} {cx},{top + 104} {cx - 100},{top + 52}" fill="{p["node"]}" stroke="{ink}" stroke-width="1"/>'

    line = f'stroke="{m}" stroke-width="1.2" marker-end="url(#arrow)"'
    style_block = f"\n        <style>{font_face}</style>" if font_face else ""
    # vertical rhythm inside boxes grows with the hand ramp
    n_y, d1_y, d2_y = (446, 468, 488) if hand else (448, 466, 482)
    end_h = 72 if hand else 64
    e1, e2, e3 = (612, 632, 652) if hand else (610, 626, 644)
    o1, o2 = (165, 185) if hand else (166, 182)
    svg = f"""
      <svg viewBox="0 0 1000 740" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
        <title id="{slug}-title">{t["title"]}</title>
        <desc id="{slug}-desc">{t["desc"]}</desc>{style_block}
        <defs>
          <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
            <circle cx="1" cy="1" r="0.9" fill="{p["dots"]}"/>
          </pattern>
          <marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{m}"/></marker>
          <marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{acc}"/></marker>
        </defs>

        <rect width="100%" height="100%" fill="{p["paper"]}"/>
        <rect width="100%" height="100%" fill="url(#dots)" opacity="0.55"/>

        <!-- Arrows (drawn first, behind nodes) -->
        <line x1="500" y1="88" x2="500" y2="120" {line}/>
        <line x1="400" y1="172" x2="300" y2="172" {line}/>
        <line x1="600" y1="172" x2="700" y2="172" {line} stroke-dasharray="5,4"/>
        <line x1="500" y1="224" x2="500" y2="272" {line}/>
        <path d="M400,324 H188 Q180,324 180,332 V424" fill="none" {line}/>
        <line x1="500" y1="376" x2="500" y2="424" {line}/>
        <path d="M600,324 H812 Q820,324 820,332 V424" fill="none" {line}/>
        <path d="M180,504 V540 Q180,548 188,548 H492" fill="none" stroke="{m}" stroke-width="1.2"/>
        <path d="M820,504 V540 Q820,548 812,548 H508" fill="none" stroke="{m}" stroke-width="1.2"/>
        <line x1="500" y1="504" x2="500" y2="544" stroke="{m}" stroke-width="1.2"/>
        <line x1="500" y1="552" x2="500" y2="588" stroke="{acc}" stroke-width="1.4" marker-end="url(#arrow-accent)"/>

        <!-- Arrow labels -->
        {arrow_label(350, 172 - 8 - sz["mask_h"], t["lbl"]["just"])}
        {arrow_label(650, 172 - 8 - sz["mask_h"], t["lbl"]["dec"])}
        {beside(500, 240, t["lbl"]["bar"])}
        {arrow_label(290, 324 - 8 - sz["mask_h"], t["lbl"]["alt"])}
        {beside(500, 392, t["lbl"]["dep"])}
        {arrow_label(710, 324 - 8 - sz["mask_h"], t["lbl"]["rng"])}

        <!-- Start -->
        {oval(360, 40, 280, 48)}
        {txt(500, 68, t["start"], sz["name"], 600)}

        <!-- Decision 1 -->
        {diamond(500, 120)}
        {txt(500, 168, t["d1"][0], sz["name"], 600)}
        {txt(500, 184, t["d1"][1], sz["name"], 600)}

        <!-- Speed end -->
        {oval(60, 148, 240, 48)}
        {txt(180, o1, t["speed"][0], sz["name"], 600)}
        {txt(180, o2, t["speed"][1], sz["sub"], None, m, mono)}

        <!-- best-minds hand-off -->
        {oval(700, 148, 240, 48)}
        {txt(820, o1, t["bm"][0], sz["name"], 600)}
        {txt(820, o2, t["bm"][1], sz["sub"], None, m, mono)}

        <!-- Decision 2 -->
        {diamond(500, 272)}
        {txt(500, 328, t["d2"], sz["name"], 600)}

        <!-- Axis steps -->
        {box(60, 424, 240, 80)}
        {txt(180, n_y, t["alt"][0], sz["name"], 600)}
        {txt(180, d1_y, t["alt"][1], sz["desc"], None, m)}
        {txt(180, d2_y, t["alt"][2], sz["desc"], None, m)}

        {box(380, 424, 240, 80)}
        {txt(500, n_y, t["dep"][0], sz["name"], 600)}
        {txt(500, d1_y, t["dep"][1], sz["desc"], None, m)}
        {txt(500, d2_y, t["dep"][2], sz["desc"], None, m)}

        {box(700, 424, 240, 80)}
        {txt(820, n_y, t["rng"][0], sz["name"], 600)}
        {txt(820, d1_y, t["rng"][1], sz["desc"], None, m)}
        {txt(820, d2_y, t["rng"][2], sz["desc"], None, m)}

        <!-- Merge point -->
        <circle cx="500" cy="548" r="4" fill="{ink}"/>

        <!-- End (focal) -->
        {oval(340, 588, 320, end_h, p["tint"], acc)}
        {txt(500, e1, t["end"][0], sz["name"], 600)}
        {txt(500, e2, t["end"][1], sz["name"], 600)}
        {txt(500, e3, t["end"][2], sz["sub"], None, m, mono)}

        <!-- Legend -->
        <line x1="40" y1="676" x2="960" y2="676" stroke="{p["rule"]}" stroke-width="0.8"/>
        {txt(40, 692, t["legend_title"], sz["ltitle"], None, m, mono, anchor=None, extra=' letter-spacing="0.18em"')}

        <rect x="40" y="708" width="24" height="12" rx="6" fill="{p["oval"]}" stroke="{p["oval_stroke"]}" stroke-width="1"/>
        {txt(72, 718, t["legend"][0], sz["legend"], None, m, anchor=None)}
        <rect x="200" y="708" width="24" height="12" rx="2" fill="{p["node"]}" stroke="{ink}" stroke-width="1"/>
        {txt(232, 718, t["legend"][1], sz["legend"], None, m, anchor=None)}
        <polygon points="372,714 384,708 396,714 384,720" fill="{p["node"]}" stroke="{ink}" stroke-width="1"/>
        {txt(408, 718, t["legend"][2], sz["legend"], None, m, anchor=None)}
        <circle cx="556" cy="714" r="4" fill="{ink}"/>
        {txt(568, 718, t["legend"][3], sz["legend"], None, m, anchor=None)}
        <line x1="632" y1="716" x2="660" y2="716" stroke="{acc}" stroke-width="1.4" marker-end="url(#arrow-accent)"/>
        {txt(668, 718, t["legend"][4], sz["legend"], None, m, anchor=None)}
        <line x1="752" y1="716" x2="780" y2="716" stroke="{m}" stroke-width="1.2" marker-end="url(#arrow)"/>
        {txt(788, 718, t["legend"][5], sz["legend"], None, m, anchor=None)}
        <line x1="856" y1="716" x2="884" y2="716" stroke="{m}" stroke-width="1.2" stroke-dasharray="5,4" marker-end="url(#arrow)"/>
        {txt(892, 718, t["legend"][6], sz["legend"], None, m, anchor=None)}
      </svg>"""

    font_link = "" if hand else f'\n  <link href="{FONT_LINK[lang]}" rel="stylesheet">'
    page_face = f"\n    {font_face}" if font_face else ""
    return f"""<!DOCTYPE html>
<html lang="{f["lang"]}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t["title"]}</title>{font_link}
  <style>{page_face}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --color-paper:   {p["paper"]};
      --color-ink:     {ink};
      --color-muted:   {m};
      --color-accent:  {acc};
      --font-sans:     {sans};
      --font-serif:    {f["serif"]};
      --font-mono:     {mono};
    }}

    body {{
      font-family: var(--font-sans);
      background: var(--color-paper);
      color: var(--color-ink);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 3rem 2rem;
    }}

    .frame {{ max-width: 1200px; width: 100%; min-width: 0; }}
    .diagram-container {{ width: 100%; overflow-x: auto; }}

    .eyebrow {{
      font-family: var(--font-mono);
      font-size: 0.66rem;
      font-weight: 500;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--color-muted);
      margin-bottom: 0.5rem;
    }}

    h1 {{
      font-family: var(--font-serif);
      font-size: clamp(1.5rem, 2.4vw + 0.75rem, 2rem);
      font-weight: 400;
      letter-spacing: -0.02em;
      line-height: 1.15;
      color: var(--color-ink);
      margin-bottom: 1.5rem;
    }}

    svg {{ width: 100%; min-width: 1000px; display: block; }}
    @media print {{
      .diagram-container {{ overflow-x: visible; }}
      svg {{ min-width: 0; }}
    }}
  </style>
</head>
<body>
  <div class="frame">
    <p class="eyebrow">{t["eyebrow"]}</p>
    <h1>{t["h1"]}</h1>

    <div class="diagram-container">{svg}
    </div>
  </div>
</body>
</html>
"""


if __name__ == "__main__":
    # Usage:
    #   gen_flow.py            write the four Geist/Noto HTML sources
    #   gen_flow.py --hand     also write the two zh-TW handwriting sources and the font subsets
    #   gen_flow.py --inject <svg>...   embed the matching font subset into exported SVGs
    # The HTML sources never embed fonts (diagram-design's self-check forbids data: URLs
    # in CSS); the subsets live in fonts/ and go into the exported SVGs, where a GitHub
    # README <img> cannot load web fonts.
    if "--inject" in sys.argv:
        for arg in sys.argv[sys.argv.index("--inject") + 1:]:
            inject_faces(Path(arg).resolve())
        sys.exit(0)
    for theme in ("light", "dark"):
        name = "ambition-flow" + ("-dark" if theme == "dark" else "") + ".html"
        (OUT / name).write_text(build("en", theme), encoding="utf-8")
        print("wrote", name)
    if "--noto" in sys.argv:  # the Geist + Noto Sans TC zh-TW pair, kept for comparison only
        for theme in ("light", "dark"):
            name = "ambition-flow-zh-TW" + ("-dark" if theme == "dark" else "") + ".html"
            (OUT / name).write_text(build("zh", theme), encoding="utf-8")
            print("wrote", name)
    if "--hand" in sys.argv:
        hand_font_face()
        geist_font_faces()
        for theme in ("light", "dark"):
            name = "ambition-flow-zh-TW-hand" + ("-dark" if theme == "dark" else "") + ".html"
            (OUT / name).write_text(build("zh", theme, hand=True), encoding="utf-8")
            print("wrote", name)
