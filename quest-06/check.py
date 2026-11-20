"""関数のページをチェックし、合格したら単語を表示します。

  python check.py --stage 1
  python check.py --stage 2

このチェッカーが確かめられるのは、ページの形だけです。中身のよさまではわかりません。
書いたページを読み、「新しく来た仲間が、これを読んでこの関数を使えるか？」と自分に聞いてみましょう。
"""
import argparse
import base64
import doctest
import importlib.util
import inspect
import io
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE = "delivery_time.md"
HEADINGS = ["Parameters", "Returns", "Example"]
WORDS = {1: "aGVhZGxpbmU=", 2: "c2FtcGxl"}


def sections(text):
    """Split the page into {heading: body}. The part before the first '## ' is called ''."""
    result = {"": []}
    current = ""
    for line in text.splitlines():
        match = re.match(r"##\s+(.+?)\s*#*\s*$", line)
        if match:
            current = match.group(1)
            result.setdefault(current, [])
        else:
            result[current].append(line)
    return {key: "\n".join(lines).strip() for key, lines in result.items()}


def words(text):
    return re.findall(r"[A-Za-z0-9']+", re.sub(r"`[^`]*`", "x", text))


def structure_problems(text, name):
    """Stage 1 rules: the title, a summary, and the three headings in order."""
    problems = []
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines or lines[0].strip() != f"# {name}()":
        problems.append(f"1行目はタイトルにしてください: # {name}()")
    intro = sections(text)[""].splitlines()[1:] if lines else []
    summary = " ".join(line.strip() for line in intro if line.strip())
    if not summary:
        problems.append("タイトルの下に、関数が何をするかを1文で書いてください。")
    # only TODO at the start of a line is left from the template; "no TODO" in a sentence is fine
    elif any(re.match(r"\s*TODO\b", line) for line in intro):
        problems.append("タイトルの下の TODO を、関数が何をするかを書いた1文に置き換えてください。")
    else:
        if not summary[0].isupper():
            problems.append("要約の文は大文字で始めてください。")
        if not summary.endswith("."):
            problems.append("要約の文の最後は '.' にしてください。")
        if len(re.findall(r"[.!?](?:\s|$)", summary)) > 1:
            problems.append("要約は1文です。詳しいことは下の節に書いてください。")
    found = [h for h in sections(text) if h]
    for heading in HEADINGS:
        if heading not in found:
            problems.append(f"見出しを追加してください: ## {heading}")
    order = [h for h in found if h in HEADINGS]
    if len(order) == len(HEADINGS) and order != HEADINGS:
        problems.append("見出しはこの順に並べてください: " + ", ".join(HEADINGS))
    return problems


def content_problems(text, params):
    """Stage 2 rules: every parameter is in the list, with its default value; Returns says what comes back."""
    parts = sections(text)
    problems = []
    items = [re.sub(r"^\s*[-*]\s+", "", line) for line in parts.get("Parameters", "").splitlines()
             if re.match(r"^\s*[-*]\s+", line)]
    documented = {}
    for item in items:
        match = re.match(r"`(\w+)`", item)
        if not match:
            problems.append(f"項目は、- `name`: のように、バッククォートで囲んだ引数名で始めてください: {item!r}")
            continue
        documented[match.group(1)] = item
    for name in documented:
        if name not in params:
            problems.append(f"関数に `{name}` という引数はありません。つづりを確かめてください。")
    for name, default in params.items():
        item = documented.get(name)
        if item is None:
            problems.append(f"## Parameters の下のリストに、引数 `{name}` のことを書いてください。")
            continue
        if len(words(item)) < 4:
            problems.append(f"`{name}` についてもう少し書きましょう。何を表すか、どんな種類の値（数、文字列など）か。")
        if default is not None and ("default" not in item.lower() or default.strip("'\"") not in item):
            problems.append(f"`{name}` には既定値があります。'Default: `{default}`.' のように書いてください。")
    if len(words(parts.get("Returns", ""))) < 3:
        problems.append("## Returns の下に、関数が何を返すかを書いてください。")
    return problems


def shorten(output):
    """Show only the last line of a traceback: the name of the error and its message."""
    lines = [line.strip() for line in output.strip().splitlines() if line.strip()]
    if not lines:
        return "(nothing)"
    if lines[0].startswith("Traceback"):
        return lines[-1]
    return "\n                        ".join(lines)


def example_problems(text, globs, name):
    """Stage 2 rules: the examples in the python code blocks work."""
    blocks = re.findall(r"^```(?:python|py|pycon)?[ \t]*\n(.*?)^```", sections(text).get("Example", ""),
                        re.S | re.M)
    code = "\n".join(blocks)
    parser = doctest.DocTestParser()
    test = parser.get_doctest(code, dict(globs), name, PAGE, 0)
    if len(test.examples) < 2:
        return ["## Example の下に、コードブロックで例を2つ以上書いてください:\n"
                "        ```python\n        >>> ...\n        ...\n        ```"]
    out = io.StringIO()
    runner = doctest.DocTestRunner(optionflags=doctest.NORMALIZE_WHITESPACE)
    runner.run(test, out=out.write)
    if not runner.failures:
        return []
    problems = []
    for block in out.getvalue().split("*" * 70):
        match = re.search(r"Failed example:\n\s+(.+?)\n(Expected:\n(.*?)\nGot:?\n?(.*)|Exception raised:\n(.*))",
                          block, re.S)
        if not match:
            continue
        example = match.group(1).strip()
        if match.group(5):
            error = match.group(5).strip().splitlines()[-1].strip()
            problems.append(f">>> {example}\n        エラーになりました: {error}")
        else:
            expected, got = shorten(match.group(3)), shorten(match.group(4))
            problems.append(f">>> {example}\n        ページの記述: {expected}\n        Python の出力: {got}")
    return problems or ["動かない例があります。例を1つずつ Python で実行し、出力をそのまま写してください。"]


def report(title, problems):
    if problems:
        print(f"[{title}]")
        for p in problems:
            print(f"    - {p}")
        return 1
    print(f"[{title}] OK")
    return 0


def check_page(text, name, params, globs, part):
    """Stage 1: the structure and the content. Stage 2: the examples too."""
    failed = report("形", structure_problems(text, name))
    if not failed:
        failed += report("中身", content_problems(text, params))
    if part >= 2 and not failed:
        failed += report("例", example_problems(text, globs, name))
    return failed


def delivery():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("delivery", HERE / "delivery.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    func = module.delivery_time
    params = {p.name: (None if p.default is inspect.Parameter.empty else repr(p.default))
              for p in inspect.signature(func).parameters.values()}
    return params, vars(module)


def main():
    parser = argparse.ArgumentParser(description="関数のページをチェックします。",
                                     epilog="例: python check.py --stage 1")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2], required=True, help="チェックするステージの番号")
    args = parser.parse_args()

    params, globs = delivery()
    text = (HERE / PAGE).read_text(encoding="utf-8")
    failed = check_page(text, "delivery_time", params, globs, args.part)

    print()
    if failed:
        print("まだです。上の問題を直して、もう一度チェックしてください。")
        return 1
    print(f"ステージ {args.part} 合格！")
    print(f"ステージ {args.part} の答えになる単語: {base64.b64decode(WORDS[args.part]).decode()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
