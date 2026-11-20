"""Checks for pull requests: title style, protected files, relative links in Markdown,
and TODO left in the class assignments (team/ and welcome/)."""
import fnmatch
import os
import re
import subprocess
import sys
from pathlib import Path

TYPES = ["feat", "fix", "docs", "style", "refactor", "test", "chore"]
TITLE_RE = re.compile(r"^(?P<type>[a-z]+)(\([\w\-]+\))?!?: (?P<subject>.+)$")
PROTECTED = ["quest-*/quest.py", "quest-*/stages.json", ".github/*", "LICENSE"]
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
ASSIGNMENT_DIRS = ("team/", "welcome/")  # the team page (Quest 14) and the welcome quests (classes 14 and 15)
TEMPLATE_DIR = "welcome/_template/"      # the template itself is full of TODO


def check_title(title):
    problems = []
    m = TITLE_RE.match(title.strip())
    if not m:
        return ["タイトルは `type: subject` の形にしてください（例: `docs: fix a typo in quest-00`）。"]
    if m.group("type") not in TYPES:
        problems.append(f"`{m.group('type')}` という type はありません。次のどれかを使ってください: {', '.join(TYPES)}")
    first = m.group("subject").split()[0]
    if re.match(r"^[a-z]+ed$", first.lower()):
        problems.append(f"`{first}` は過去形のようです。原形にしてください（たとえば `fixed` ではなく `fix`）。")
    return problems


def changed_files(base, head):
    out = subprocess.run(["git", "diff", "--name-only", f"{base}...{head}"],
                         text=True, capture_output=True, check=True).stdout
    return [f for f in out.splitlines() if f]


def check_protected(files):
    bad = [f for f in files if any(fnmatch.fnmatch(f, p) for p in PROTECTED)]
    if not bad:
        return []
    return ["これらのファイルはメンテナーが管理しています。変更しないでください"
            "（代わりに Issue を出してください）: " + ", ".join(f"`{f}`" for f in bad)]


def check_links(files):
    problems = []
    for name in files:
        path = Path(name)
        if path.suffix.lower() != ".md" or not path.is_file():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for target in LINK_RE.findall(line):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue  # web links and anchors are not checked
                file_part = target.split("#", 1)[0]
                if file_part and not (path.parent / file_part).exists():
                    problems.append(f"`{name}` の {lineno} 行目のリンクが切れています: `{target}` は存在しません。")
    return problems


def check_todo(files):
    problems = []
    for name in files:
        path = Path(name)
        if not name.startswith(ASSIGNMENT_DIRS) or name.startswith(TEMPLATE_DIR) or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # not a text file
        for lineno, line in enumerate(text.splitlines(), start=1):
            if "TODO" in line:
                problems.append(f"`{name}` の {lineno} 行目に `TODO` が残っています。ひな型の `TODO` は、すべて書きかえてください。")
    return problems


def main():
    title = os.environ.get("PR_TITLE", "")
    files = changed_files(os.environ["BASE_SHA"], os.environ["HEAD_SHA"])
    results = [
        ("タイトル", check_title(title)),
        ("保護されたファイル", check_protected(files)),
        ("リンク", check_links(files)),
        ("書き残し（TODO）", check_todo(files)),
    ]
    lines = ["| チェック | 結果 |", "|---|---|"]
    failed = False
    for name, problems in results:
        if problems:
            failed = True
            for p in problems:
                print(f"❌ {name}: {p}")
                lines.append(f"| {name} | ❌ {p} |")
        else:
            print(f"✅ {name}: OK")
            lines.append(f"| {name} | ✅ OK |")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("## プルリクエストのチェック\n\n" + "\n".join(lines) + "\n")
    if failed:
        tips = []
        if results[0][1]:  # the title can be fixed with Edit on GitHub; no push is needed
            tips.append("タイトルは、プルリクエストの画面の Edit で直してください。")
        if any(problems for _, problems in results[1:]):
            tips.append("ファイルは、直して同じブランチに push してください。")
        print("\n" + "".join(tips) + "直すと、チェックがもう一度動きます。")
        sys.exit(1)


if __name__ == "__main__":
    main()
