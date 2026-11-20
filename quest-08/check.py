"""バグ報告をチェックし、合格したら単語を表示します。

  python check.py --stage 1
  python check.py --stage 2

このチェッカーが確かめられるのは、報告の形だけです。わかりやすさまではわかりません。
班の人に手順をたどってもらいましょう。同じバグが見えますか？
"""
import argparse
import base64
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HEADINGS = ["Steps to reproduce", "Expected", "Actual", "Environment"]
WORDS = {1: "bGFiZWw=", 2: "cmVwcm8="}
VAGUE_TITLES = {"bug", "error", "help", "broken", "problem", "issue", "urgent", "it does not work", "doesn't work"}
OS_NAMES = ("windows", "macos", "mac os", "linux", "ubuntu", "codespaces")


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
    problems = []
    # only TODO at the start of a line is left from the template; "no TODO" in a sentence is fine
    if not title or re.match(r"TODO\b", title):
        problems.append("1行目にタイトルを書いてください: '# Your title'")
    for name in HEADINGS:
        if name not in sections:
            problems.append(f"見出し '## {name}' がありません。見出しを消したり、名前を変えたりしないでください。")
        elif not sections[name] or re.search(r"^\s*TODO\b", sections[name], flags=re.M):
            problems.append(f"'## {name}' がまだ空です。TODO をあなたの文に置き換えてください。")
    return problems


def find_commands(steps):
    """Commands in `inline code` that start with python."""
    return [c.strip() for c in re.findall(r"`([^`\n]+)`", steps) if re.match(r"\s*python3?\s+\S", c)]


def run_command(command):
    parts = shlex.split(command, posix=(os.name != "nt"))
    parts[0] = sys.executable
    result = subprocess.run(parts, cwd=HERE, capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
    return result.returncode, result.stderr.strip()


def form_problems(title, sections, require_run):
    """Stage 2 and 3 rules."""
    problems = []
    words = re.findall(r"[A-Za-z0-9_.']+", title)
    if len(words) < 4 or title.lower().strip(" .!?") in VAGUE_TITLES:
        problems.append("タイトルがあいまいです。何が起きるかを、4〜10語くらいで書いてください。"
                        "例: 'Crash when the tool gets an empty file'")
    steps = sections.get("Steps to reproduce", "")
    numbered = re.findall(r"^\s*\d+\.\s+\S", steps, flags=re.M)
    if len(numbered) < 2:
        problems.append("手順は番号つきのリストで、2つ以上書いてください: '1. ...' と '2. ...'")
    env = sections.get("Environment", "")
    if not re.search(r"python\s*3\.\d+", env, flags=re.I):
        problems.append("Environment: 'Python 3.12' のように Python のバージョンを書いてください。確認: python --version")
    if not any(name in env.lower() for name in OS_NAMES):
        problems.append("Environment: 'Linux'、'Windows 11'、'macOS' のように OS を書いてください。（Codespaces は Linux です）")
    if sections.get("Expected", "").strip() == sections.get("Actual", "").strip():
        problems.append("'Expected' と 'Actual' が同じです。Expected は「起きるべきこと」、Actual は「実際に起きること」です。")
    if require_run:
        commands = find_commands(steps)
        if not commands:
            problems.append("手順の中に、コマンドをバッククォートで囲んで書いてください。例: `python tip.py 50 2`")
        else:
            code, err = run_command(commands[-1])
            last = err.splitlines()[-1] if err else ""
            if code == 0:
                problems.append(f"`{commands[-1]}` を実行しましたが、エラーで止まりませんでした。このクエストでは、エラーで止まるバグを報告します。")
            elif last and last not in sections.get("Actual", ""):
                problems.append("'Actual' には、実際のエラーの最後の行をそのまま写してください。実行した結果:\n"
                                f"        {last}")
    return problems


def main():
    parser = argparse.ArgumentParser(description="バグ報告をチェックします。",
                                     epilog="例: python check.py --stage 1")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2], required=True, help="チェックするステージの番号")
    args = parser.parse_args()

    try:
        text = (HERE / "issue.md").read_text(encoding="utf-8")
    except OSError:
        sys.exit("Cannot read issue.md. quest-08 フォルダで実行してください。")
    title, sections = parse(text)
    problems = basic_problems(title, sections)
    if not problems and args.part == 2:
        problems = form_problems(title, sections, require_run=True)

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
