"""プルリクエストのタイトルと説明文をチェックし、合格したら単語を表示します。

  python check.py --stage 1
  python check.py --stage 2
  python check.py --stage 3     （あなたが現場に出した、いちばん新しいプルリクエストをチェック）

このチェッカーが確かめられるのは形だけです。英語のわかりやすさまではわかりません。
「レビューする人が、diff を読む前にこの変更を理解できるか？」と自分に聞いてみましょう。
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
TYPES = ["feat", "fix", "docs", "style", "refactor", "test", "chore"]
PATTERN = re.compile(r"^(?P<type>[a-z]+)(\([\w\-]+\))?!?: (?P<subject>.+)$")
HEADINGS = ["Summary", "Changes", "How to test"]
ISSUE = 52
WORDS = {1: "YmFubmVy", 2: "Ymx1ZXByaW50", 3: "ZGVidXQ="}


def title_problems(title, need_type=None):
    """The same rules as commit messages: 'type: subject'."""
    if not title or re.match(r"TODO\b", title):
        return ["1行目にタイトルを書いてください。例: '# fix: stop the crash when the bag is full'"]
    m = PATTERN.match(title)
    if not m:
        return ["'type: subject' の形にしてください（例: 'fix: stop the crash when the bag is full'）。"]
    problems = []
    if m.group("type") not in TYPES:
        problems.append(f"'{m.group('type')}' という type はありません。次のどれかを使ってください: {', '.join(TYPES)}")
    elif need_type and m.group("type") != need_type:
        problems.append(f"この変更はバグ（Issue #{ISSUE}）を直すものです。バグの修正に使う type はどれですか？")
    first = m.group("subject").split()[0]
    if first[0].isupper():
        problems.append("subject は小文字で始めてください。")
    if re.fullmatch(r"[a-z]+ed", first.lower()):
        problems.append(f"動詞は原形にしてください: '{first}' ではいけません。たとえば 'fixed' ではなく 'fix' です。")
    if title.endswith("."):
        problems.append("タイトルの最後にピリオドをつけないでください。")
    if len(title) > 72:
        problems.append(f"タイトルが長すぎます（{len(title)} 文字）。72文字以内にしてください。")
    if len(m.group("subject").split()) < 3:
        problems.append("subject をもう少し詳しく書いてください（3語以上）。")
    return problems


def parse(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)  # the comments of the pull request template are not counted
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


def body_problems(sections, files=None, issue=None):
    problems = []
    for name in HEADINGS:
        # only a line that starts with TODO (as in pr.md) is left from the template; "no TODO" in a sentence is fine
        if not sections.get(name) or re.search(r"^\s*TODO\b", sections[name], flags=re.M):
            problems.append(f"'## {name}' の節を書いてください。（`<!-- -->` のコメントの中に書いた文は数えません）")
    if problems:
        return problems
    whole = "\n".join(sections.values())
    closes = re.findall(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", whole, flags=re.I)
    if issue is not None:
        if not closes:
            problems.append(f"プルリクエストがマージされたときに閉じるように、Issue をつなげてください: 'Closes #{ISSUE}'")
        elif any(int(n) != issue for n in closes):
            problems.append(f"Issue の番号を確かめてください。この変更は Issue #{ISSUE} のためのものです。")
    elif not closes:
        problems.append("'Closes #3' のように、あなたが立てた Issue をつなげてください。")
    if len(re.findall(r"\w+", sections["Summary"])) < 8:
        problems.append("'Summary': 何をなぜ変えたかを、1〜2文で書いてください。")
    if files is not None:
        changes = sections["Changes"]
        for f in files:
            if f not in changes:
                problems.append(f"'Changes': '{f}' は diff にあります。そのファイルで何が変わったかを書いてください。")
        for f in re.findall(r"`([\w./-]+\.\w+)`", changes):
            if f not in files:
                problems.append(f"'Changes': '{f}' は diff にありません。本当に変わったものだけを書いてください。")
    if len(re.findall(r"^\s*\d+\.\s+\S", sections["How to test"], flags=re.M)) < 2:
        problems.append("'How to test': 手順を番号つきのリストで、2つ以上書いてください。")
    return problems


def diff_files():
    text = (HERE / "change.diff").read_text(encoding="utf-8")
    return re.findall(r"^diff --git a/(\S+) ", text, flags=re.M)


def api(url, missing_ok=False):
    """Read the GitHub API. In Codespaces, GITHUB_TOKEN raises the limit. Without it, try again with no token."""
    headers = {"User-Agent": "quest-checker", "Accept": "application/vnd.github+json"}
    error = None
    for token in ([os.environ.get("GITHUB_TOKEN")] if os.environ.get("GITHUB_TOKEN") else []) + [None]:
        h = dict(headers, **({"Authorization": f"Bearer {token}"} if token else {}))
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=20) as r:
                return json.loads(r.read().decode("utf-8"))
        except OSError as err:
            if missing_ok and getattr(err, "code", None) == 404:
                return None
            error = err
    sys.exit(f"GitHub を読めません（{url}）: {error}\n1分待ってから、もう一度試してください。")


def fork_and_upstream(fork=None):
    """Find your fork (from 'git remote') and the quest repository it was forked from."""
    if fork is None:
        result = subprocess.run(["git", "remote", "get-url", "origin"], cwd=HERE, capture_output=True, text=True)
        m = re.search(r"github\.com[/:]([\w.-]+)/([\w.-]+?)(?:\.git)?/?$", result.stdout.strip())
        if result.returncode != 0 or not m:
            sys.exit("あなたの fork がわかりません。fork の名前を指定してください: python check.py --stage 3 YOUR-ID/REPO")
        fork = f"{m.group(1)}/{m.group(2)}"
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", fork):
        sys.exit(f"'{fork}' は YOUR-ID/REPO の形になっていません。")
    repo = api(f"https://api.github.com/repos/{fork}", missing_ok=True)
    if repo is None:
        sys.exit(f"{fork} が見つかりません。名前を確かめてください。")
    if not repo.get("parent"):
        sys.exit(f"{fork} は fork ではありません。現場の fork で実行してください。")
    return fork.split("/")[0], repo["parent"]["full_name"]


def page_problems(me, files):
    names = [f["filename"] for f in files]
    page = f"team/{me}.md"
    if [n.lower() for n in names] != [page.lower()]:
        return [f"このプルリクエストで変えるのは '{page}' の1つだけにしてください。いま変わっているファイル: {', '.join(names) or 'なし'}"]
    added = [line[1:] for line in (files[0].get("patch") or "").splitlines()
             if line.startswith("+") and not line.startswith("+++")]
    text = "\n".join(added)
    problems = []
    if "TODO" in text:
        problems.append(f"'{page}' に TODO が残っています。すべて書きかえてください。")
    if not added or not re.match(r"#\s+\S", added[0]):
        problems.append(f"'{page}' の1行目は、'# {me}' のような見出しにしてください。")
    if len(re.findall(r"^\s*[-*]\s+\S", text, flags=re.M)) < 2:
        problems.append(f"'{page}' の2つの節に、'- ' で始まる項目を1つずつ書いてください。")
    if re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", text):
        problems.append(f"'{page}' は英語で書いてください。")
    return problems


def part3(fork):
    me, upstream = fork_and_upstream(fork)
    mine = [p for p in api(f"https://api.github.com/repos/{upstream}/pulls?state=all&per_page=100")
            if p["user"]["login"].lower() == me.lower()]
    if not mine:
        sys.exit(f"{upstream} に、{me} さんのプルリクエストが見つかりません。"
                 "Create pull request を押しましたか？（README.md の ステージ 3 を見てください）")
    pr = mine[0]
    print(f"{upstream} のプルリクエスト #{pr['number']} をチェックします: {pr['title']}")
    title, sections = parse("# " + pr["title"] + "\n" + (pr.get("body") or ""))
    problems = title_problems(title) or body_problems(sections)
    if problems:
        return problems
    number = int(re.findall(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", "\n".join(sections.values()),
                            flags=re.I)[0])
    issue = api(f"https://api.github.com/repos/{upstream}/issues/{number}", missing_ok=True)
    if issue is None or "pull_request" in issue:
        return [f"#{number} という Issue はありません。あなたが立てた Issue の番号を書いてください。"]
    if issue["user"]["login"].lower() != me.lower():
        return [f"#{number} は {issue['user']['login']} さんの Issue です。あなたが立てた Issue の番号を書いてください。"]
    return page_problems(me, api(f"https://api.github.com/repos/{upstream}/pulls/{pr['number']}/files"))


def main():
    parser = argparse.ArgumentParser(description="プルリクエストのタイトルと説明文をチェックします。",
                                     epilog="例: python check.py --stage 3")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2, 3], required=True, help="チェックするステージの番号")
    parser.add_argument("fork", nargs="?", help="ステージ 3 だけ（ふつうは不要）: あなたの fork の YOUR-ID/REPO")
    args = parser.parse_args()

    if args.part < 3:
        title, sections = parse((HERE / "pr.md").read_text(encoding="utf-8"))
        problems = title_problems(title, need_type="fix")
        if args.part == 2 and not problems:
            problems = body_problems(sections, diff_files(), ISSUE)
    else:
        problems = part3(args.fork)

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
