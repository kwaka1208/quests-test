"""The history of Northwind's app: a small git repository with 50 commits.

  python history.py --setup   make the history (or make it again from the start)
  python history.py           check that the history is ready
"""
import argparse
import base64
import os
import random
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE / "history"
PEOPLE = ["Misaki", "Haruto", "Yui", "Daiki", "Kaito"]
TOPICS = ["login", "search", "payment", "upload", "timeout", "export", "cache", "email", "report", "backup"]
# One word for each commit. The first one belongs to Daiki's commit about the backup.
WORDS = [
    "Y2hlY2twb2ludA==", "cGViYmxl", "ZmVhdGhlcg==", "a2V0dGxl", "cmliYm9u", "dGhpbWJsZQ==",
    "YWNvcm4=", "YnV0dG9u", "YnVja2V0", "bGFkZGVy", "bWFyYmxl", "bmVlZGxl",
    "cGlsbG93", "c2FkZGxl", "dGVhcG90", "d2FsbnV0", "YW5jaG9y", "YmFza2V0",
    "Y29id2Vi", "Z29ibGV0", "aGVsbWV0", "bGl6YXJk", "bWl0dGVu", "b3lzdGVy",
    "cGFycm90", "cXVpbGw=", "cmFiYml0", "c3Bvb24=", "dHVybmlw", "dmlvbGlu",
    "d2hpc3RsZQ==", "YXByb24=", "YmFycmVs", "Y2FjdHVz", "ZG9scGhpbg==", "ZW5naW5l",
    "ZmFsY29u", "Z2FybGlj", "aGFtbW9jaw==", "aWdsb28=", "amlnc2F3", "a2l0dGVu",
    "bGVtb24=", "bWFnbmV0", "bm9vZGxl", "b3JjaGlk", "cGVwcGVy", "cm9ja2V0",
    "dHVsaXA=", "d2Fnb24=",
]
TARGET = ("Daiki", "backup")


def git(*args, check=True, who="Misaki", date=None):
    """Run git in the history. The commits are made by the team, not by you."""
    cmd = ["git", "-C", str(REPO), "-c", f"user.name={who}", "-c", f"user.email={who.lower()}@northwind.invalid",
           "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *args]
    env = dict(os.environ)
    if date:
        env.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if check and result.returncode != 0:
        sys.exit(f"git {' '.join(args)} が失敗しました:\n{result.stderr}")
    return result


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def commits():
    """Every person works on every topic once, in a fixed random order."""
    pairs = [(who, topic) for who in PEOPLE for topic in TOPICS]
    pairs.remove(TARGET)
    random.Random(3).shuffle(pairs)
    words = [base64.b64decode(w).decode() for w in WORDS]
    chosen = dict(zip(pairs, words[1:]))
    chosen[TARGET] = words[0]
    order = pairs[:]
    order.insert(31, TARGET)
    return [(who, topic, chosen[(who, topic)]) for who, topic in order]


def setup():
    if REPO.exists():
        if sys.version_info >= (3, 12):
            shutil.rmtree(REPO, onexc=remove_readonly)
        else:
            shutil.rmtree(REPO, onerror=remove_readonly)
    REPO.mkdir()
    git("init", "-q")
    git("symbolic-ref", "HEAD", "refs/heads/main")
    for number, (who, topic, word) in enumerate(commits()):
        path = REPO / f"{topic}.txt"
        with path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(f"A change by {who}.\n")
        date = f"2026-01-{1 + number // 10:02d}T{9 + number % 10:02d}:00:00+00:00"
        git("add", path.name)
        git("commit", "-q", "-m", f"Fix a bug in {topic}",
            "-m", f"The code word of this commit is: {word}", who=who, date=date)
    print(f"'history' フォルダに履歴を用意しました。コミットは {len(WORDS)} 個あります。")
    print()
    print("次にすること:")
    print("    cd history")
    print("    git log")


def check():
    if not (REPO / ".git").exists():
        print("履歴がまだありません。実行: python history.py --setup")
        return 1
    count = git("rev-list", "--count", "HEAD", check=False).stdout.strip()
    if count != str(len(WORDS)):
        print("履歴が変わっているようです。`python history.py --setup` で作り直してください。")
        return 1
    print(f"履歴は用意できています。コミットは {count} 個です。")
    print("'history' フォルダに移動して、`git log` で探しましょう。")
    return 0


def main():
    parser = argparse.ArgumentParser(description="The history of Northwind's app.")
    parser.add_argument("--setup", action="store_true", help="make the history again from the start")
    args = parser.parse_args()
    if shutil.which("git") is None:
        print("git が見つかりません。Codespaces を使ってください。")
        return 1
    if args.setup:
        setup()
        return 0
    return check()


if __name__ == "__main__":
    sys.exit(main())
