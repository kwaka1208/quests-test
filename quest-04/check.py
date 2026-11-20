"""help の文をチェックし、合格したら単語を表示します。

  python check.py --stage 1
  python check.py --stage 2

このチェッカーが確かめられるのは、help の形だけです。中身のよさまではわかりません。
書いた help を声に出して読み、「初めての人の役に立つか？」と自分に聞いてみましょう。
"""
import argparse
import base64
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_LENGTH = 60
# Words that do not explain anything by themselves.
EMPTY_WORDS = {"a", "an", "the", "of", "to", "for", "in", "on", "at", "is", "it", "this", "that", "and", "or",
               "option", "value", "argument", "set", "sets", "use", "uses", "default", "flag", "command"}
WORDS = {1: "Y2xhcml0eQ==", 2: "aG9yaXpvbg=="}
BAD_PERCENT = "help の中で '%' を表示するには '%%' と書きます。例: 'more than 50%% of the sales'"


def name_of(action):
    return "/".join(action.option_strings) or action.dest


def expand(text, params):
    """Show the text as --help shows it, without breaking on a wrong '%'."""
    text = re.sub(r"%\((\w+)\)s", lambda m: str(params.get(m.group(1), m.group(0))), text)
    return text.replace("%%", "%")


def help_problems(text, names, params=None):
    """Stage 1 rules: the help is there, short, and written like other command-line tools."""
    if not text or not text.strip():
        return ["help が空です。何をするオプションかを書いてください。"]
    problems = []
    shown = expand(text, params or {})
    first = re.match(r"[A-Za-z0-9]+", shown)
    if not first or (shown[0].isupper() and not re.fullmatch(r"[A-Z0-9]{2,}s?", first.group())):
        problems.append("'show' や 'how many' のように、小文字で始めてください。（'RGB' のような略語は大文字でかまいません）")
    if shown.rstrip().endswith("."):
        problems.append("最後に '.' をつけないでください。たいていのツールは、help に '.' をつけません。")
    if len(shown) > MAX_LENGTH:
        problems.append(f"help が長すぎます（{len(shown)} 文字）。{MAX_LENGTH} 文字以内にしてください。")
    words = set(re.findall(r"[a-z]+", re.sub(r"%\(\w+\)s", "", text).lower()))
    own = set(re.findall(r"[a-z]+", " ".join(names).lower()))
    if not words - own - EMPTY_WORDS:
        problems.append("help が名前をくり返しているだけです。何をするか、または何を指定するのかを書いてください。")
    return problems


def load_parser():
    """Run build_parser() from report.py, and return the parser."""
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("report", HERE / "report.py")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except SyntaxError as err:
        sys.exit(f"report.py の {err.lineno} 行目に文法エラーがあります: {err.msg}\n"
                 "help の文のまわりの引用符（ \" ）とカンマ（ , ）を確かめてください。")
    try:
        return module.build_parser()
    except ValueError as err:
        sys.exit(f"report.py がエラーで止まります: {err}\n{BAD_PERCENT}")


def show_help(parser):
    """Return the problem if --help cannot be shown."""
    try:
        parser.format_help()
    except (ValueError, TypeError, KeyError) as err:
        return f"--help がエラーで止まります: {err}\n    {BAD_PERCENT}"
    return None


def check_arguments(parser, part):
    failed = 0
    for action in parser._actions:
        if isinstance(action, argparse._HelpAction):
            continue
        params = dict(vars(action), prog=parser.prog)
        if action.choices is not None:
            params["choices"] = ", ".join(map(str, action.choices))
        names = action.option_strings + [action.dest, action.metavar or ""]
        problems = help_problems(action.help, names, params)
        if part >= 2 and not problems and action.option_strings and action.nargs != 0 \
                and action.default is not None and "%(default)s" not in action.help:
            problems.append(f"このオプションには既定値（{action.default}）があります。"
                            "'(default: %(default)s)' のように、%(default)s で表示してください。")
        if problems:
            failed += 1
            print(f"[{name_of(action)}] {action.help!r}")
            for p in problems:
                print(f"    - {p}")
        else:
            print(f"[{name_of(action)}] OK")
    return failed


def description_problems(text):
    if not text or not text.strip():
        return ["description が空です。ツールについて1文で書いてください。"]
    problems = []
    text = text.strip()
    if not text[0].isupper():
        problems.append("description は大文字で始めてください。")
    if not text.endswith("."):
        problems.append("description の最後は '.' にしてください。")
    if len(re.findall(r"[.!?](?:\s|$)", text)) > 1 or "\n" in text:
        problems.append("1文だけにしてください。ツール全体が何をするかを書きます。")
    return problems


def check_report(part):
    parser = load_parser()
    failed = check_arguments(parser, part)
    if part >= 2:
        problem = show_help(parser)
        if problem:
            print(f"[--help] {problem}")
            failed += 1
        problems = description_problems(parser.description)
        if problems:
            failed += 1
            print(f"[description] {(parser.description or '').strip()!r}")
            for p in problems:
                print(f"    - {p}")
        else:
            print("[description] OK")
    return failed


def main():
    parser = argparse.ArgumentParser(description="help の文をチェックします。",
                                     epilog="例: python check.py --stage 1")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2], required=True, help="チェックするステージの番号")
    args = parser.parse_args()

    failed = check_report(args.part)

    print()
    if failed:
        print("まだです。上の問題を直して、もう一度チェックしてください。")
        return 1
    print(f"ステージ {args.part} 合格！")
    print(f"ステージ {args.part} の答えになる単語: {base64.b64decode(WORDS[args.part]).decode()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
