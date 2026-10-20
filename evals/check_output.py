"""判斷受測輸出是不是異常：空輸出、殘缺片段、推理外洩、把工具呼叫寫成純文字。

用法：python3 -I evals/check_output.py <輸出檔> <測試 prompt>
正常時不印任何東西、exit 0；異常時印一行原因、exit 1。
每條規則都對應一次實測看過的異常（2026-10-20）：
  - 殘缺片段「，沒有 Skill tool 調用，應直接回答。Range 軸。」
  - 開頭外洩英文推理「見 wait: The ambition skill is loaded as system prompt? ...」
  - 整份輸出是英文推理「rt with the skill invoked. The user's task: ...」
  - 沒有工具時把 <invoke name="Bash"> 寫成純文字
"""
import re
import sys

MIN_CHARS = 40
LEAK_MARKERS = re.compile(
    r"\bthe user'?s?\b|system prompt|\bthe skill\b|\blet me\b|\bI should\b|\bI need to\b|\bwait:|<invoke name=|<parameter name=",
    re.IGNORECASE,
)
CJK = re.compile(r"[㐀-鿿豈-﫿]")


def reason(text: str, prompt: str) -> str:
    body = text.strip()
    if len(body) < MIN_CHARS:
        return f"輸出過短（{len(body)} 字）"
    if body[0] in "，。、；：！？）」』,.;:!?)" or re.match(r"[a-z]", body):
        return f"輸出從句子中間開始：{body[:30]!r}"
    head = body[:400]
    m = LEAK_MARKERS.search(head)
    if m:
        return f"開頭有推理外洩的用語：{m.group(0)!r}"
    if CJK.search(prompt):
        sample = re.sub(r"\s", "", body)[:200]
        ratio = len(CJK.findall(sample)) / max(len(sample), 1)
        if ratio < 0.2:
            return f"任務是中文，開頭的中文字比例只有 {ratio:.0%}"
    if "<invoke name=" in body:
        return "把工具呼叫寫成純文字"
    return ""


def main() -> int:
    path, prompt = sys.argv[1], sys.argv[2]
    with open(path, encoding="utf-8") as f:
        r = reason(f.read(), prompt)
    if r:
        print(r)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
