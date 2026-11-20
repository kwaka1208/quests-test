"""ベータ版の前夜の作業をチェックし、合格したら単語を表示します。

  python check.py --stage 1                       （server.py の ERRORS と help の文）
  python check.py --stage 2                       （bug-report.md と commit.txt）

決まりは、Quest 2・4・8 と同じです。
"""
import argparse
import base64
import importlib.util
import re
import shlex
import string
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORDS = {1: "a2luZGxl", 2: "cGF0Y2g="}
COLD = ["stupid", "idiot", "dumb", "illegal", "fatal", "invalid", "bad", "go away"]
ACTIONS = {"try", "type", "use", "check", "choose", "pick", "run", "start", "stop", "close", "wait", "ask", "add", "write"}
EMPTY = {"a", "an", "the", "of", "to", "for", "in", "on", "at", "is", "it", "this", "that", "and", "or",
         "option", "value", "argument", "set", "sets", "use", "uses", "default", "flag"}
TYPES = ["feat", "fix", "docs", "style", "refactor", "test", "chore"]


def report(title, problems):
    if problems:
        print(f"[{title}]")
        for p in problems:
            print(f"    - {p}")
        return 1
    print(f"[{title}] OK")
    return 0


# ---------- Stage 1: ERRORS (Quest 2) and help (Quest 4) ----------

def error_problems(message):
    if not message.strip():
        return ["メッセージが空です。"]
    problems = []
    plain = re.sub(r"\{[^}]*\}", "", message)
    if [w for w in re.findall(r"[A-Za-z]+", plain) if len(w) >= 3 and w.isupper()]:
        problems.append("叫ばないでください。大文字だけの単語を書かないでください。")
    if "!!" in message:
        problems.append("'!' は1つで十分です。使わなくてもかまいません。")
    for word in COLD:
        if re.search(r"\b" + word + r"\b", message.lower()):
            problems.append(f"'{word}' は冷たく、失礼に聞こえます。何が起きたかを、ふつうの言葉で書きましょう。")
    try:
        names = {n for _, n, _, _ in string.Formatter().parse(message) if n}
    except ValueError:
        return problems + ["'{' か '}' が閉じていません。"]
    if names - {"env", "port"}:
        problems.append("使えるプレースホルダーは {env} と {port} だけです。")
    if not names:
        problems.append("プレースホルダー {env} か {port} を使って、相手に情報を見せましょう。")
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", message.strip()) if s]
    if len(sentences) < 2 or not message.rstrip().endswith((".", "!", "?")):
        problems.append("短い文を2つ書いてください。「何が起きたか」と「次に何をすればよいか」です。")
    elif not any(re.sub(r"^[^A-Za-z]+", "", s).split(" ")[0].lower() in ACTIONS for s in sentences):
        problems.append("次に何をすればよいかを伝えましょう。'Try' や 'Use' のような動詞で始まる文を書いてください。")
    return problems


def help_problems(action):
    text = action.help or ""
    if not text.strip():
        return ["help が空です。何をするオプションかを書いてください。"]
    problems = []
    shown = re.sub(r"%\(\w+\)s", "x", text)
    if shown[0].isupper():
        problems.append("小文字で始めてください。")
    if shown.rstrip().endswith("."):
        problems.append("最後に '.' をつけないでください。")
    if len(shown) > 60:
        problems.append("60文字以内にしてください。")
    words = set(re.findall(r"[a-z]+", shown.lower())) - EMPTY - set(re.findall(r"[a-z]+", " ".join(action.option_strings)))
    if not words - {"x"}:
        problems.append("名前をくり返すだけにしないでください。何をするかを書きます。")
    if action.default is not None and "%(default)s" not in text:
        problems.append("%(default)s で既定値を表示してください。")
    return problems


def part1():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("server", HERE / "server.py")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        parser = module.build_parser()
        parser.format_help()
    except (SyntaxError, ValueError, TypeError, KeyError) as err:
        sys.exit(f"server.py がエラーで止まります: {err}\n引用符・カンマ・'%' を確かめてください。")
    failed = 0
    for key in ("port_in_use", "unknown_env"):
        failed += report(f"ERRORS['{key}']", error_problems(module.ERRORS.get(key, "")))
    for action in parser._actions:
        if action.option_strings and action.dest != "help":
            failed += report(f"{action.option_strings[0]} の help", help_problems(action))
    return failed


# ---------- Stage 2: bug report (Quest 8) and commit message ----------

def parse(text):
    title, sections, current = "", {}, None
    for line in text.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("## "):
            current = line[3:].strip().rstrip(":")
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return title, {k: "\n".join(v).strip() for k, v in sections.items()}


def bug_problems(text):
    title, s = parse(text)
    problems = []
    # only TODO at the start of a line is left from the template; "no TODO" in a sentence is fine
    if not title or re.match(r"TODO\b", title) or len(title.split()) < 4:
        problems.append("何が起きるかがわかるタイトルを書いてください（4語以上）。")
    for name in ("Steps to reproduce", "Expected", "Actual", "Environment"):
        if not s.get(name) or re.search(r"^\s*TODO\b", s[name], flags=re.M):
            problems.append(f"'## {name}' の節を書いてください。")
    if problems:
        return problems
    if len(re.findall(r"^\s*\d+\.\s+\S", s["Steps to reproduce"], flags=re.M)) < 2:
        problems.append("手順を番号つきのリストで、2つ以上書いてください。")
    if not re.search(r"python\s*3\.\d+", s["Environment"], flags=re.I):
        problems.append("Environment: 'Python 3.12' のように Python のバージョンを書いてください。")
    commands = [c for c in re.findall(r"`([^`\n]+)`", s["Steps to reproduce"]) if re.match(r"python3?\s", c)]
    if not commands:
        problems.append("手順の中に、コマンドをバッククォートで囲んで書いてください。")
        return problems
    parts = shlex.split(commands[-1])
    parts[0] = sys.executable
    result = subprocess.run(parts, cwd=HERE, capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
    last = (result.stderr.strip().splitlines() or [""])[-1]
    if result.returncode == 0:
        problems.append(f"`{commands[-1]}` を実行したら、問題なく動きました。この手順ではバグが見えません。")
    elif last not in s["Actual"]:
        problems.append(f"'Actual' には、実際のエラーの最後の行を写してください:\n        {last}")
    return problems


def commit_problems(text):
    first = text.strip().splitlines()[0] if text.strip() else ""
    m = re.match(r"^(?P<type>[a-z]+)(\([\w\-]+\))?!?: (?P<subject>.+)$", first)
    if not first or re.match(r"TODO\b", first) or not m:
        return ["1行目を 'type: subject' の形にしてください。"]
    problems = []
    if m.group("type") != "fix":
        problems.append("このコミットはバグを直すものです。バグの修正に使う type はどれですか？")
    word = m.group("subject").split()[0]
    if word[0].isupper() or re.fullmatch(r"[a-z]+ed", word.lower()):
        problems.append("subject は、'stop' のように、小文字の原形の動詞で始めてください。")
    if first.endswith(".") or len(first) > 72:
        problems.append("最後にピリオドをつけず、72文字以内にしてください。")
    return problems


def part2():
    failed = report("bug-report.md", bug_problems((HERE / "bug-report.md").read_text(encoding="utf-8")))
    failed += report("commit.txt", commit_problems((HERE / "commit.txt").read_text(encoding="utf-8")))
    return failed


def main():
    parser = argparse.ArgumentParser(description="ベータ版の前夜の作業をチェックします。",
                                     epilog="例: python check.py --stage 1")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2], required=True, help="チェックするステージの番号")
    args = parser.parse_args()

    failed = part1() if args.part == 1 else part2()

    print()
    if failed:
        print("まだです。上の問題を直して、もう一度チェックしてください。")
        return 1
    print(f"ステージ {args.part} 合格！")
    print(f"ステージ {args.part} の答えになる単語: {base64.b64decode(WORDS[args.part]).decode()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
