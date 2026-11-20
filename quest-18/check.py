"""コードレビューをチェックし、合格したら単語を表示します。

  python check.py --stage 1
  python check.py --stage 2
  python check.py --stage 3 NUMBER     （現場の、班の人のプルリクエストへのあなたのレビュー）

このチェッカーが確かめられるのは、レビューの形だけです。自分に聞いてみましょう。
「このレビューをもらったらうれしいか？ 作者がコードを直す助けになるか？」
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
LABELS = ("blocking", "nit", "question", "optional")
DECISIONS = ("Approve", "Comment", "Request changes")
RUDE = ["stupid", "terrible", "bad code", "wrong!", "!!", "obviously", "you never", "you always", "lazy"]
BUG_LINE = 8
WORDS = {1: "Y291cnRlc3k=", 2: "c3BvdGxpZ2h0", 3: "bWVudG9y"}


def parse(text):
    decision = None
    comments = []
    for line in text.splitlines():
        m = re.match(r"\s*Decision:\s*(.*)$", line)
        if m:
            decision = m.group(1).strip()
        m = re.match(r"\s*[-*]\s*line\s+(\S+)\s*:\s*(\w+)\s*:\s*(.*)$", line, flags=re.I)
        if m:
            comments.append((m.group(1), m.group(2).lower(), m.group(3).strip()))
    return decision, comments


def comment_problems(label, text, where):
    problems = []
    if label not in LABELS:
        problems.append(f"{where}: ラベルで始めてください: {', '.join(l + ':' for l in LABELS)}")
    if len(re.findall(r"[A-Za-z']+", text)) < 5:
        problems.append(f"{where}: もう少し書いてください（5語以上）。何が問題で、何を変えるべきか。")
    for word in RUDE:
        if word in text.lower():
            problems.append(f"{where}: '{word}' は失礼に聞こえます。人ではなく、コードについて書きましょう。")
    return problems


def form_problems(decision, comments, lines):
    problems = []
    if not decision or re.match(r"TODO\b", decision):
        problems.append("1行目に判断を書いてください: 'Decision: Approve'、'Comment'、'Request changes' のどれか")
    elif decision not in DECISIONS:
        problems.append(f"判断は次のどれかにしてください: {', '.join(DECISIONS)}")
    if len(comments) < 3:
        problems.append("コメントを3つ以上、1行に1つずつ書いてください: '- line 8: blocking: ...'")
    for number, label, text in comments:
        where = f"line {number}"
        if not number.isdigit() or not 1 <= int(number) <= lines:
            problems.append(f"{where}: stock.py の行は 1〜{lines} です。実際にある行番号を書いてください。")
            continue
        problems += comment_problems(label, text, where)
    if not any(label == "question" and "?" in text for _, label, text in comments):
        problems.append("'question:' のラベルをつけ、'?' のついた質問を1つ書いてください。")
    return problems


def bug_problems(decision, comments):
    problems = []
    blocking = [(int(n), t) for n, l, t in comments if l == "blocking" and n.isdigit()]
    if not any(n == BUG_LINE for n, _ in blocking):
        problems.append("本物のバグがあります。'python try_stock.py' を実行して、説明文をもう一度読みましょう。"
                        "その行を見つけて、'blocking:' をつけてください。")
    for n, _ in blocking:
        if n != BUG_LINE:
            problems.append(f"line {n}: これは本当にバグですか？ 名前のような小さなことは 'nit:' か 'optional:' です。")
    for n, t in blocking:
        if n == BUG_LINE and not re.search(r"\b(should|please|could|use|change|try|need)\b", t.lower()):
            problems.append(f"line {n}: 'This should be ...' のように、作者が何をすればよいかを書いてください。")
    if blocking and decision != "Request changes":
        problems.append("blocking の問題を見つけました。合う判断はどれですか？")
    return problems


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


def part3(number, fork=None):
    me, repo = fork_and_upstream(fork)
    base = f"https://api.github.com/repos/{repo}/pulls/{number}"
    pr = api(base, missing_ok=True)
    if pr is None:
        sys.exit(f"{repo} に、#{number} というプルリクエストはありません。番号を確かめてください。")
    if pr["user"]["login"].lower() == me.lower():
        sys.exit("これはあなた自身のプルリクエストです。班の人のプルリクエストをレビューしてください。")
    texts = [r.get("body") or "" for r in api(base + "/reviews") if r["user"]["login"].lower() == me.lower()]
    texts += [c.get("body") or "" for c in api(base + "/comments") if c["user"]["login"].lower() == me.lower()]
    texts = [t.strip() for t in texts if t.strip()]
    print(f"プルリクエスト #{number}: {pr['title']} — {me} さんのレビューの文が {len(texts)} 個見つかりました。")
    problems = []
    if not texts:
        problems.append(f"{me} さんのレビューが見つかりません。'Submit review' を押しましたか？")
    # a label in bold (**nit:** or **nit**:), as quest-17 shows it, counts too
    labeled = [m for m in (re.match(r"[*_\s]*(blocking|nit|question|optional)[*_]*\s*:[*_]*(.*)", t, flags=re.I | re.S)
                           for t in texts) if m]
    if len(labeled) < 2:
        problems.append("ラベル（blocking:、nit:、question:、optional:）で始まるコメントを2つ以上書いてください。")
    for i, m in enumerate(labeled, 1):
        problems += comment_problems(m.group(1).lower(), m.group(2), f"comment {i}")
    return problems


def main():
    parser = argparse.ArgumentParser(description="コードレビューをチェックします。",
                                     epilog="例: python check.py --stage 3 12")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2, 3], required=True, help="チェックするステージの番号")
    parser.add_argument("number", nargs="?", help="ステージ 3 だけ: レビューしたプルリクエストの番号")
    parser.add_argument("fork", nargs="?", help="ステージ 3 だけ（ふつうは不要）: あなたの fork の YOUR-ID/REPO")
    args = parser.parse_args()
    if args.part < 3:
        decision, comments = parse((HERE / "review.md").read_text(encoding="utf-8"))
        lines = len((HERE / "stock.py").read_text(encoding="utf-8").splitlines())
        problems = form_problems(decision, comments, lines)
        if args.part == 2 and not problems:
            problems = bug_problems(decision, comments)
    else:
        if not args.number or not args.number.lstrip("#").isdigit():
            parser.error("ステージ 3 には、レビューしたプルリクエストの番号が必要です（例: python check.py --stage 3 12）")
        problems = part3(args.number.lstrip("#"), args.fork)
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
