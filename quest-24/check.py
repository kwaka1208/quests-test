"""仕様書をチェックし、合格したら単語を表示します。

  python check.py --stage 1
  python check.py --stage 2

このチェッカーが確かめられるのは形だけです。「ほかの班の人が、この仕様書だけを読んで、正しいファイルを書けるか？」と
自分に聞いてみましょう。
"""
import argparse
import base64
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORDS = {1: "Y2hhcnRlcg==", 2: "Y29ybmVyc3RvbmU="}
KEYWORDS = ["MUST NOT", "SHOULD NOT", "MUST", "SHOULD", "MAY"]
FIELDS = ["version", "card", "points", "history", "date", "change", "note"]


def sections(text):
    result, current = {}, None
    for line in text.splitlines():
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            current = m.group(1)
            result[current] = []
        elif current:
            result[current].append(line)
    return {k: "\n".join(v).strip() for k, v in result.items()}


def rules(text):
    """Numbered rules in '## Rules': {number: text}. A rule can go on over several lines."""
    out, current = {}, None
    for line in sections(text).get("Rules", "").splitlines():
        m = re.match(r"^\s*(\d+)\.\s+(.*)$", line)
        if m:
            current = int(m.group(1))
            out[current] = m.group(2)
        elif current and line.strip():
            out[current] += " " + line.strip()
    return out


def keywords_in(rule):
    found = []
    rest = re.sub(r"`[^`]*`", "", rule)
    for k in KEYWORDS:
        n = len(re.findall(r"\b" + k + r"\b", rest))
        found += [k] * n
        rest = re.sub(r"\b" + k + r"\b", "", rest)
    return found


def form_problems(text, minimum=5, example=True):
    problems = []
    first = next((l for l in text.splitlines() if l.strip()), "")
    # only TODO at the start of a line is left from the template; "no TODO" in a sentence is fine
    if not first.startswith("# ") or re.match(r"#\s*TODO\b", first):
        problems.append("1行目に仕様書の名前を書いてください: '# ...'")
    if "RFC 2119" not in sections(text).get("Keywords", ""):
        problems.append("'## Keywords' に、キーワードを RFC 2119 のとおりに使うことを書いてください。")
    r = rules(text)
    if len(r) < minimum:
        problems.append(f"'## Rules' に、番号つきの決まりを {minimum} 個以上書いてください: '1. ...', '2. ...'")
    if r and sorted(r) != list(range(1, len(r) + 1)):
        problems.append("決まりの番号は、1, 2, 3, ... と飛ばさずにつけてください。")
    for n, rule in sorted(r.items()):
        found = keywords_in(rule)
        lower = re.search(r"\b(must|should|may)\b", re.sub(r"`[^`]*`", "", rule))
        if not found and not lower:
            problems.append(f"Rule {n}: キーワード（MUST、MUST NOT、SHOULD、SHOULD NOT、MAY）が入っていません。1つ入れてください。")
        elif len(found) > 1:
            problems.append(f"Rule {n}: キーワードはちょうど1つにしてください。いまは {len(found)} 個あります。2つの決まりに分けましょう。")
        if re.search(r"\b(must|should|may)\b", re.sub(r"`[^`]*`", "", rule)):
            problems.append(f"Rule {n}: キーワードは MUST のように大文字で書いてください。")
    # the example is the work of stage 2, so stage 1 does not look at its TODO
    checked = text if example else re.sub(r"^## Example\s*$.*?(?=^## |\Z)", "", text, flags=re.M | re.S)
    if re.search(r"^[#\s]*TODO\b", checked, flags=re.M):
        problems.append("TODO をすべて置き換えてください。")
    return problems


def example_json(text):
    m = re.search(r"```(?:json)?\s*\n(.*?)```", sections(text).get("Example", ""), flags=re.S)
    return m.group(1) if m else None


def content_problems(text):
    r = rules(text)
    all_rules = " ".join(r.values()).lower()
    problems = []
    for field in FIELDS:
        if not re.search(r"\b" + field + r"\b", all_rules):
            problems.append(f"'{field}' について書いた決まりがありません。例にあるフィールドには、どれも決まりが必要です。")
    if not any("name" in rule.lower() and "MUST NOT" in keywords_in(rule) for rule in r.values()):
        problems.append("チームは「客の名前は決してファイルに入れない」と決めました。'never' を表すキーワードはどれですか？")
    if not any("note" in rule.lower() and "MAY" in keywords_in(rule) for rule in r.values()):
        problems.append("変更には、望むならメモをつけられます。'if you want' を表すキーワードはどれですか？")
    if not any(("100" in rule) and keywords_in(rule) and keywords_in(rule)[0].startswith("SHOULD") for rule in r.values()):
        problems.append("最新の100件だけを残すのは「そのほうがよい」ことで、エラーではありません。合うキーワードはどれですか？")
    block = example_json(text)
    if block is None:
        problems.append("'## Example' に、コードブロック（```json ... ```）で例のファイルを入れてください。")
    else:
        try:
            data = json.loads(block)
        except ValueError as err:
            problems.append(f"例が正しい JSON になっていません: {err}")
        else:
            for field in ("version", "card", "points", "history"):
                if field not in data:
                    problems.append(f"例に '{field}' がありません。例は、あなた自身の決まりに従っている必要があります。")
    return problems


def main():
    parser = argparse.ArgumentParser(description="仕様書をチェックします。",
                                     epilog="例: python check.py --stage 1")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2], required=True, help="チェックするステージの番号")
    args = parser.parse_args()

    text = (HERE / "SPEC.md").read_text(encoding="utf-8")
    problems = form_problems(text, example=args.part == 2)
    if args.part == 2 and not problems:
        problems = content_problems(text)

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
