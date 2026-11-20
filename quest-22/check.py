"""devlog をチェックし、合格したら単語を表示します。

  python check.py --stage 1
  python check.py --stage 2

このチェッカーが確かめられるのは形だけです。「クラスメイトが楽しく読めて、何かを学べるか？」と自分に聞いてみましょう。
"""
import argparse
import base64
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORDS = {1: "Y2hhcHRlcg==", 2: "aW5zaWdodGZ1bA=="}


def strip(text):
    """The text without code blocks and inline code."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^(    |\t).*$", " ", text, flags=re.M)
    return re.sub(r"`[^`]*`", "x", text)


def words(text):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.-]*", text)


def form_problems(text, minimum=100):
    problems = []
    lines = [l for l in text.splitlines() if l.strip()]
    # only TODO at the start of a line is left from the template; "no TODO" in a sentence is fine
    if not lines or not lines[0].startswith("# ") or re.match(r"#\s*TODO\b", lines[0]):
        problems.append("1行目にタイトルを書いてください: '# ...'")
    tldr = next((l for l in lines[1:] if l.strip()), "")
    if not re.match(r"\**TL;DR:?\**", tldr.strip()):
        problems.append("タイトルのすぐ下に、TL;DR の行を書いてください: 'TL;DR: ...'")
    elif re.match(r"\**TL;DR:?\**\s*TODO\b", tldr.strip()) or len(words(tldr)) < 6:
        problems.append("TL;DR を書いてください。話全体を、短い1〜2文で書きます。")
    elif len(words(tldr)) > 40:
        problems.append("TL;DR が長すぎます。40語以内にしてください。")
    headings = [l for l in lines if l.startswith("## ")]
    if len(headings) < 2 or any(re.match(r"##\s*TODO\b", h) for h in headings):
        problems.append("'The problem' や 'What I did' のような見出し（'## ...'）を2つ以上書いてください。")
    if re.search(r"^[#\s]*TODO\b", text, flags=re.M):
        problems.append("TODO をすべて置き換えてください。")
    body = strip("\n".join(l for l in text.splitlines() if not l.startswith("#")))
    count = len(words(body))
    if count < minimum:
        problems.append(f"記事は {count} 語です。{minimum}語以上書いてください。")
    if count > 300:
        problems.append(f"記事は {count} 語です。300語以内にしてください。")
    return problems


def content_problems(text, link):
    body = strip("\n".join(l for l in text.splitlines() if not l.startswith("#")))
    problems = []
    if not re.search(r"\bbecause\b", body, flags=re.I):
        problems.append("'because' を使って、判断の理由を書いてください: 'I chose ... because ...'")
    if not re.search(r"\b(but|however|trade-off|tradeoff)\b", body, flags=re.I):
        problems.append("比べてください。'but'、'however'、'trade-off' を使って、選ばなかったものを書きます。")
    if not re.search(link, text):
        problems.append("修正のプルリクエストにリンクしてください: '#58'（または URL）と書きます。")
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", body)) if len(words(s)) >= 1]
    if sentences:
        average = sum(len(words(s)) for s in sentences) / len(sentences)
        if average > 20:
            problems.append(f"文の長さが平均 {average:.0f} 語です。もっと短くしてください（20語以下）。")
    if re.search(r"[぀-ヿ一-鿿]", text):
        problems.append("記事は英語だけで書いてください。")
    return problems


def main():
    parser = argparse.ArgumentParser(description="devlog をチェックします。",
                                     epilog="例: python check.py --stage 1")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2], required=True, help="チェックするステージの番号")
    args = parser.parse_args()

    text = (HERE / "devlog.md").read_text(encoding="utf-8")
    problems = form_problems(text)
    if args.part == 2 and not problems:
        problems = content_problems(text, r"(#58\b|/pull/58\b)")

    if problems:
        for p in problems:
            print(f"  - {p}")
        print()
        print("まだです。上の問題を直して、もう一度チェックしてください。")
        return 1
    print(f"ステージ {args.part} 合格！")
    print(f"ステージ {args.part} の答えになる単語: {base64.b64decode(WORDS[args.part]).decode()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
