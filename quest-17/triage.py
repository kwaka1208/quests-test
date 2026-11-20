"""triage.txt をチェックします（ステージ1）。このファイルは編集しないでください。実行: python triage.py"""
import base64
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = {"approved_by": "a2FpdG8=", "must_fix_lines": "MTU=", "reply_only_lines": "MTg=",
            "free_to_skip_lines": "MTAsMTksMjM="}


def main():
    answers = {}
    for line in (HERE / "triage.txt").read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        answers[key.strip()] = value.strip().lower().lstrip("@")
    for key in EXPECTED:
        if not answers.get(key):
            sys.exit(f"'{key}:' が空です。triage.txt の行をすべて埋めてください。")
        if key != "approved_by" and not re.fullmatch(r"\d+(\s*,\s*\d+)*", answers[key]):
            sys.exit(f"'{key}:' には、カンマで区切った行番号を書いてください。例: 3, 8")
    for key, secret in EXPECTED.items():
        expected = base64.b64decode(secret).decode()
        given = answers[key]
        if key == "approved_by":
            given = given.split("-")[0]  # "kaito-m" (the GitHub ID) is OK, too
        else:
            given = ",".join(sorted((n.strip() for n in given.split(",")), key=int))
        if given != expected:
            print("まだです。少なくとも1行がまちがっています。（どの行かは教えません）")
            print("それぞれのレビューの種類と、それぞれのコメントのラベルを見直しましょう。")
            return 1
    print("正解！ すべてのレビューとコメントを仕分けられました。")
    print("Code word:", base64.b64decode("YmFsYW5jZQ==").decode())
    return 0


if __name__ == "__main__":
    sys.exit(main())
