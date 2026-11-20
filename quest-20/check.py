"""CHANGELOG をチェックし、合格したら単語を表示します。

  python check.py --stage 1
  python check.py --stage 2 YOUR-ID

このチェッカーが確かめられるのは形だけです。「利用者が、何が変わったか、自分は何をすればよいかがわかるか？」と自分に聞いてみましょう。
"""
import argparse
import base64
import datetime
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORDS = {1: "bWlsZXN0b25l", 2: "Y3JlZGl0cw=="}
SECTIONS = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]
# What each user-facing commit is about. A line in the CHANGELOG must mention one of the words.
ADDED = {"予約注文（pre-orders）": ["pre-order", "preorder"], "設定 points_per_dollar": ["points_per_dollar"]}
FIXED = {"ポイントの丸め（round half up）": ["round"],
         "在庫の最後の品物（the last items in the stock）": ["stock", "last item", "all the items", "all items"],
         "返金のときのポイント（refund points）": ["refund", "return", "taken back", "take back", "takes back"]}
NOT_FOR_USERS = {"README の変更（docs）": ["readme"], "税の定数の整理（refactor）": ["constant"],
                 "テストの追加（test）": ["tests for", "add tests", "added tests", "unit test", "the tests"]}
AUTHORS = ["@haruto-cto", "@kaito-m", "@daiki-ops", "@haruka-m"]


def versions(text):
    """{version: {section: [items]}} and the list of headers, in order."""
    result, order = {}, []
    version = section = None
    for line in text.splitlines():
        m = re.match(r"^## \[(.+?)\](.*)$", line)
        if m:
            version, section = m.group(1), None
            result[version] = {"_header": line}
            order.append(version)
            continue
        m = re.match(r"^### (.+?)\s*$", line)
        if m and version:
            section = m.group(1)
            result[version][section] = []
            continue
        if section and re.match(r"^\s*[-*]\s+\S", line):
            result[version][section].append(line.strip()[1:].strip())
    return result, order


def date_problem(header):
    m = re.search(r"\]\s*-\s*(\S+)\s*$", header)
    if not m:
        return "バージョンの後ろに日付を書いてください。例: '## [2.0.0] - 2026-12-01'"
    try:
        datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return "日付は 2026-12-01 のように YYYY-MM-DD の形で書いてください。"
    return None


def mentions(items, words):
    return any(w in item.lower() for item in items for w in words)


def part1(text):
    v, _ = versions(text)
    if "2.0.0" not in v:
        return ["'## [2.0.0] - ...' の行は残してください。"]
    rel = v["2.0.0"]
    problems = [p for p in [date_problem(rel["_header"])] if p]
    for s in rel:
        if s != "_header" and s not in SECTIONS:
            problems.append(f"'### {s}' は Keep a Changelog の節ではありません。使えるのは: {', '.join(SECTIONS)}")
    for name, words in ADDED.items():
        if not mentions(rel.get("Added", []), words):
            problems.append(f"'### Added': {name} についての行を書いてください。")
    for name, words in FIXED.items():
        if not mentions(rel.get("Fixed", []), words):
            problems.append(f"'### Fixed': {name} についての行を書いてください。")
    everything = [i for s, items in rel.items() if s != "_header" for i in items]
    for name, words in NOT_FOR_USERS.items():
        if any(re.search(r"\b" + w + r"s?\b", item.lower()) for item in everything for w in words):
            problems.append(f"{name} のことは書かないでください。利用者には見えない変更です。")
    return problems


def part2(text, me):
    problems = part1(text)
    if problems:
        return problems
    rel = versions(text)[0]["2.0.0"]
    changed = rel.get("Changed", [])
    removed = rel.get("Removed", [])
    if not mentions(changed, ["pickup"]):
        problems.append("'### Changed': 設定 pickup について書いてください（名前が変わりました）。")
    if not mentions(removed, ["quiet"]):
        problems.append("'### Removed': 設定 quiet について書いてください。")
    for section, items, word in (("Changed", changed, "pickup"), ("Removed", removed, "quiet")):
        for item in items:
            if word in item.lower() and "breaking" not in item.lower():
                problems.append(f"'### {section}': {word} の変更は古い設定を動かなくします。**BREAKING** をつけてください。")
    if not mentions(rel.get("Deprecated", []), ["points_rate"]):
        problems.append("'### Deprecated': points_rate が非推奨になったことと、代わりに何を使うかを書いてください。")
    m = re.search(r"^## Contributors\s*$(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    if not m:
        problems.append("最後に '## Contributors' の節を追加し、コミットした人を全員書いてください。")
    else:
        names = {n.lower() for n in re.findall(r"@[\w-]+", m.group(1))}
        for a in AUTHORS + ["@" + me.lstrip("@")]:
            if a.lower() not in names:
                problems.append(f"'## Contributors': {a} もコミットしています。コミットした人は、みんな貢献者（contributor）です。")
        if "@you" in names:
            problems.append("'## Contributors': @YOU ではなく、あなた自身の GitHub ID を書いてください。")
    return problems


def main():
    parser = argparse.ArgumentParser(description="CHANGELOG をチェックします。",
                                     epilog="例: python check.py --stage 2 your-id")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2], required=True, help="チェックするステージの番号")
    parser.add_argument("target", nargs="?", help="ステージ 2 だけ: あなたの GitHub ID")
    args = parser.parse_args()
    text = (HERE / "CHANGELOG.md").read_text(encoding="utf-8")
    if args.part == 1:
        problems = part1(text)
    else:
        if not args.target or "/" in args.target:
            parser.error("ステージ 2 には、あなたの GitHub ID の指定が必要です: python check.py --stage 2 YOUR-ID")
        problems = part2(text, args.target)

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
