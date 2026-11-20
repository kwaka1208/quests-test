"""Checks a question for a Q&A site, and gives you a word when it passes.

  python check.py --stage 1
  python check.py --stage 2

This checker can only check the form of a question, not how clear it is.
Read your question, and ask yourself: "Can a stranger understand my problem in one minute?"
"""
import argparse
import ast
import base64
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HEADINGS = ["What I want to do", "Code", "What happened", "What I tried"]
WORDS = {1: "cXVlcnk=", 2: "Zm9jdXM="}
VAGUE = ["urgent", "asap", "please help", "help me", "help!", "doesn't work", "does not work", "not working"]
MAX_LINES = {2: 10, 3: 15}


def parse(text):
    """Return (title, {heading: body})."""
    title = ""
    sections = {}
    current = None
    for line in text.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("## "):
            current = line[3:].strip().rstrip(":")
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return title, {k: "\n".join(v).strip() for k, v in sections.items()}


def basic_problems(title, sections):
    """Stage 1 rules: the title and the four sections are written."""
    problems = []
    # only TODO at the start of a line is left from the template; "no TODO" in a sentence is fine
    if not title or re.match(r"TODO\b", title):
        problems.append("1行目に、質問をタイトルとして書いてください: '# Your question?'")
    for name in HEADINGS:
        if name not in sections:
            problems.append(f"見出し '## {name}' がありません。見出しを消したり、名前を変えたりしないでください。")
        elif not sections[name] or re.search(r"^\s*TODO\b", sections[name], flags=re.M):
            problems.append(f"'## {name}' がまだ空です。TODO をあなたの文に置き換えてください。")
    return problems


def code_block(body):
    blocks = re.findall(r"^```(\w*)[ \t]*\n(.*?)^```", body, re.S | re.M)
    return blocks[0] if blocks else (None, "")


def form_problems(title, sections, part):
    """Stage 2 rules: a clear title, a short code block, the real output, and what you tried."""
    problems = []
    words = re.findall(r"[A-Za-z0-9_.'()]+", title)
    if not title.rstrip().endswith("?"):
        problems.append("タイトルは質問の文です。最後を '?' にしてください。")
    if len(words) < 5:
        problems.append("タイトルが短すぎます。何がおかしいのかを、5〜20語で書いてください。"
                        "例: 'Why does int(\"3.5\") give an error?'")
    if len(words) > 20:
        problems.append("タイトルが長すぎます。20語以内にして、詳しいことは本文に書いてください。")
    for word in VAGUE:
        if word in title.lower():
            problems.append(f"タイトルに '{word}' と書かないでください。何が問題なのかが伝わりません。")
    if title.isupper():
        problems.append("タイトルを大文字だけで書かないでください。")
    if len(re.findall(r"\w+", sections.get("What I want to do", ""))) < 5:
        problems.append("'What I want to do': やりたいことを、ちゃんとした文で書いてください。")
    language, code = code_block(sections.get("Code", ""))
    if language is None:
        problems.append("'Code': コードは、```python で始まり ``` で終わるコードブロックに入れてください。")
    else:
        lines = [line for line in code.splitlines() if line.strip()]
        if language.lower() not in ("python", "py"):
            problems.append("'Code': サイトが色をつけられるように、コードブロックは ```python で始めてください。")
        if len(lines) > MAX_LINES[part]:
            problems.append(f"'Code': コードが {len(lines)} 行あります。{MAX_LINES[part]} 行以内にしてください。"
                            "問題を見せるのに必要な行だけを残しましょう。")
        try:
            ast.parse(code)
        except SyntaxError as err:
            problems.append(f"'Code': コードの {err.lineno} 行目に文法エラーがあります: {err.msg}")
            code = None
        if part == 2 and code is not None and not problems:
            problems += run_problems(code, sections.get("What happened", ""))
    tried = re.findall(r"^\s*(?:[-*]|\d+\.)\s+\S", sections.get("What I tried", ""), flags=re.M)
    if not tried:
        problems.append("'What I tried': 試したことを、1行に1つずつリストで書いてください（'- ...'）。")
    return problems


def run_problems(code, happened):
    """Run the code by itself, in an empty folder. It must show the problem."""
    with tempfile.TemporaryDirectory() as folder:
        result = subprocess.run([sys.executable, "-c", code], cwd=folder, capture_output=True, text=True,
                                timeout=20, stdin=subprocess.DEVNULL)
    if result.returncode != 0:
        last = (result.stderr.strip().splitlines() or ["error"])[-1]
        return ["'Code': コードだけを実行したら、エラーで止まりました:\n"
                f"        {last}\n"
                "    読む人が実行するのは、質問の中のコードだけです。"
                "必要なものはすべてコードブロックに入れ、points.py を import しないでください。"]
    output = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not output:
        return ["'Code': コードを実行しましたが、何も表示されませんでした。おかしいと思う値を print してください。"]
    shown = {line.strip() for line in happened.splitlines()}
    if not any(line in shown for line in output):
        return ["'What happened': コードの本当の出力を、1行そのまま写してください（コードブロックがおすすめ）。実行した結果:\n"
                + "\n".join(f"        {line}" for line in output[:5])]
    return []


def main():
    parser = argparse.ArgumentParser(description="Q&A サイトに出す質問をチェックします。",
                                     epilog="例: python check.py --stage 1")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2], required=True, help="チェックするステージの番号")
    args = parser.parse_args()

    try:
        text = (HERE / "question.md").read_text(encoding="utf-8")
    except OSError:
        sys.exit("Cannot read question.md. quest-10 フォルダで実行してください。")
    title, sections = parse(text)
    problems = basic_problems(title, sections)
    if not problems and args.part == 2:
        problems = form_problems(title, sections, args.part)

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
