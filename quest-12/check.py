"""Checks docstrings, and gives you a word when they pass.

  python check.py --stage 1
  python check.py --stage 2

This checker reads the code but does not run it.
It can only check the form of a docstring. Ask yourself: "Can a teammate use this function without reading the code?"
"""
import argparse
import ast
import base64
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORDS = {1: "c3VtbWFyeQ==", 2: "c2lnbmF0dXJl"}
NOT_VERBS = {"this", "the", "a", "an", "function", "method", "it", "we", "i", "here"}
SECTIONS = ("Args:", "Returns:", "Raises:", "Yields:", "Example:", "Examples:", "Note:")


def summary_problems(doc):
    """Stage 1 rules: the first line is a short summary that starts with a verb."""
    if not doc or not doc.strip():
        return ["docstring がありません。def の行のすぐ下に、\"\"\" で囲んで書いてください。"]
    first = doc.strip().splitlines()[0].strip()
    problems = []
    word = re.sub(r"[^A-Za-z]", "", first.split()[0]) if first.split() else ""
    if not word or not word[0].isupper():
        problems.append("1行目は大文字で始めてください。")
    if word.lower() in NOT_VERBS:
        problems.append(f"'{word}' ではなく、動詞で始めてください。例: 'Return the total price.'")
    elif word.lower().endswith(("ed", "ing")) or (word.lower().endswith("s") and not word.lower().endswith("ss")):
        problems.append(f"動詞は原形にしてください: '{word}' ではなく '{base_form(word)}'")
    if not first.endswith("."):
        problems.append("1行目の最後は '.' にしてください。")
    if len(first) > 72:
        problems.append(f"1行目が長すぎます（{len(first)} 文字）。72文字以内にしてください。")
    lines = doc.strip().splitlines()
    if len(lines) > 1 and lines[1].strip():
        problems.append("1行目の後ろに、空の行を1行入れてください。")
    return problems


def base_form(word):
    w = word
    for end in ("ing", "ed", "es", "s"):
        if w.lower().endswith(end) and len(w) > len(end) + 2:
            return w[: -len(end)]
    return w


def section(doc, name):
    """Return the lines of a section like 'Args:', or None if it is not there."""
    lines = doc.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == name:
            out = []
            for nxt in lines[i + 1:]:
                if nxt.strip() in SECTIONS:
                    break
                out.append(nxt)
            return [l for l in out if l.strip()]
    return None


def detail_problems(func, doc):
    """Stage 2 rules: Args, Returns and Raises match the code."""
    problems = []
    params = [a.arg for a in func.args.posonlyargs + func.args.args + func.args.kwonlyargs if a.arg not in ("self", "cls")]
    args = section(doc, "Args:")
    if params:
        if args is None:
            problems.append("'Args:' の節を追加して、次の引数を書いてください: " + ", ".join(params))
        else:
            written = {}
            for line in args:
                m = re.match(r"\s+(\w+)\s*(\([^)]*\))?\s*:\s*(.*)", line)
                if m and len(line) - len(line.lstrip()) <= min(len(l) - len(l.lstrip()) for l in args):
                    written[m.group(1)] = m.group(3)
            for p in params:
                if p not in written:
                    problems.append(f"Args: '{p}' の行を書いてください。形は '    {p} (type): what it is.' です。")
                elif len(written[p].split()) < 3:
                    problems.append(f"Args: '{p}' についてもう少し書いてください（3語以上）。")
            for w in written:
                if w not in params:
                    problems.append(f"Args: 関数に '{w}' という引数はありません。")
    elif args is not None:
        problems.append("この関数には引数がありません。'Args:' の節を消してください。")
    returns_value = any(isinstance(n, ast.Return) and n.value is not None for n in ast.walk(func))
    rets = section(doc, "Returns:")
    if returns_value and not rets:
        problems.append("この関数は値を返します。'    type: what it is.' の形で 'Returns:' の節を追加してください（type は返す値の型）。")
    if not returns_value and rets:
        problems.append("この関数は何も返しません。'Returns:' の節を消してください。")
    raised = sorted({n.exc.func.id if isinstance(n.exc, ast.Call) and isinstance(n.exc.func, ast.Name)
                     else n.exc.id for n in ast.walk(func)
                     if isinstance(n, ast.Raise) and isinstance(getattr(n.exc, "func", n.exc), ast.Name)})
    raises = section(doc, "Raises:")
    for name in raised:
        if not raises or not any(name in line for line in raises):
            problems.append(f"この関数は {name} を起こすことがあります。'    {name}: If ...' のように 'Raises:' の節を追加してください。")
    return problems


def check_source(source, names, part, label):
    try:
        tree = ast.parse(source)
    except SyntaxError as err:
        sys.exit(f"{label} の {err.lineno} 行目に文法エラーがあります: {err.msg}")
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    failed = 0
    for name in names:
        func = funcs[name]
        doc = ast.get_docstring(func, clean=True)
        problems = summary_problems(doc)
        if part >= 2 and not problems:
            problems = detail_problems(func, doc)
        if problems:
            failed += 1
            print(f"[{name}()]")
            for p in problems:
                print(f"    - {p}")
        else:
            print(f"[{name}()] OK")
    return failed


def main():
    parser = argparse.ArgumentParser(description="docstring をチェックします。",
                                     epilog="例: python check.py --stage 1")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2], required=True, help="チェックするステージの番号")
    args = parser.parse_args()

    source = (HERE / "menu.py").read_text(encoding="utf-8")
    failed = check_source(source, ["total_price", "find_item", "print_menu"], args.part, "menu.py")

    print()
    if failed:
        print("まだです。上の問題を直して、もう一度チェックしてください。")
        return 1
    print(f"ステージ {args.part} 合格！")
    print(f"ステージ {args.part} の答えになる単語: {base64.b64decode(WORDS[args.part]).decode()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
