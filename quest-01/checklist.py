"""The release checklist of Northwind: a small git repository with a merge conflict.

  python checklist.py --setup   make the checklist (or make it again from the start)
  python checklist.py           check the checklist
"""
import argparse
import base64
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE / "checklist"
FILE = "release.txt"
TESTS = "Run all the tests."
VERSION = "Update the version number."
WORD = "dGVhbXdvcms="


def git(*args, check=True, who="Misaki"):
    """Run git in the checklist. The setup commits are made by teammates, not by you."""
    cmd = ["git", "-C", str(REPO), "-c", f"user.name={who}", "-c", f"user.email={who.lower()}@northwind.invalid",
           "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        sys.exit(f"git {' '.join(args)} が失敗しました:\n{result.stderr}")
    return result


def write(lines):
    (REPO / FILE).write_text("\n".join(lines) + "\n", encoding="utf-8")


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def setup():
    if REPO.exists():
        if sys.version_info >= (3, 12):
            shutil.rmtree(REPO, onexc=remove_readonly)
        else:
            shutil.rmtree(REPO, onerror=remove_readonly)
    REPO.mkdir()
    git("init", "-q")
    git("symbolic-ref", "HEAD", "refs/heads/main")
    git("config", "merge.conflictStyle", "merge")
    write(["Release checklist", "Step 1: Create a release branch.", "Step 2: (not written yet)",
           "Step 3: Publish the release."])
    git("add", FILE)
    git("commit", "-q", "-m", "Add the release checklist")
    git("checkout", "-q", "-b", "haruto")
    write(["Release checklist", "Step 1: Create a release branch.", f"Step 2: {VERSION}",
           "Step 3: Publish the release."])
    git("commit", "-q", "-am", "Add the version step", who="Haruto")
    git("checkout", "-q", "main")
    write(["Release checklist", "Step 1: Create a release branch.", f"Step 2: {TESTS}",
           "Step 3: Publish the release."])
    git("commit", "-q", "-am", "Add the test step")
    git("merge", "haruto", check=False)
    print("'checklist' フォルダにチェックリストを用意しました。")
    print("Misaki と Haruto が別々の手順を書いたので、git がマージできませんでした。")
    print()
    print("次にすること:")
    print("    cd checklist")
    print("    git status")


def check():
    if not (REPO / ".git").exists():
        print("チェックリストがまだありません。実行: python checklist.py --setup")
        return 1
    if (REPO / ".git" / "MERGE_HEAD").exists():
        print("マージがまだ終わっていません。checklist フォルダで `git status` の表示を読みましょう。")
        return 1
    text = (REPO / FILE).read_text(encoding="utf-8")
    if any(mark in text for mark in ("<<<<<<<", "=======", ">>>>>>>")):
        print(f"{FILE} に衝突の印（<<<<<<<、=======、>>>>>>>）が残っています。消してください。")
        return 1
    if TESTS not in text or VERSION not in text:
        print(f"2人とも正しいので、{FILE} には2人の手順を両方残してください。")
        return 1
    if git("rev-list", "--merges", "--count", "HEAD", check=False).stdout.strip() in ("", "0"):
        print("チェックリストにマージのコミットがありません。`python checklist.py --setup` からやり直してください。")
        return 1
    if git("status", "--porcelain", check=False).stdout.strip():
        print("まだコミットしていない変更があります。`git status` の表示を読みましょう。")
        return 1
    print("チェックリストが整いました。2人があなたに感謝しています。")
    print(f"合言葉: {base64.b64decode(WORD).decode()}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="The release checklist of Northwind.")
    parser.add_argument("--setup", action="store_true", help="make the checklist again from the start")
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
