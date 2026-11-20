"""クエストの出題プログラムです。このファイルは編集しないでください。

使い方は `python quest.py --help` で表示されます。
"""
import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGES_FILE = HERE / "stages.json"
PROGRESS_FILE = HERE / ".progress.json"


def normalize(answer):
    return " ".join(answer.strip().lower().split())


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_stages():
    return json.loads(STAGES_FILE.read_text(encoding="utf-8"))


def load_progress():
    try:
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_progress(progress):
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")


def make_flag(github_id, answers):
    joined = "|".join(normalize(a) for a in answers)
    return "FLAG{" + sha256(github_id.strip().lower() + "|" + joined)[:10] + "}"


def _keystream(answers, length):
    key = hashlib.sha256(("explain|" + "|".join(normalize(a) for a in answers)).encode("utf-8")).digest()
    out = b""
    counter = 0
    while len(out) < length:
        out += hashlib.sha256(key + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]


def show_explanation(quest, progress):
    """日本語の解説を表示する。すべてのステージをクリアした人だけが読める。"""
    sealed = quest.get("explanation")
    if not sealed:
        return
    answers = [progress[str(i)] for i in range(1, len(quest["stages"]) + 1)]
    data = base64.b64decode(sealed)
    text = bytes(a ^ b for a, b in zip(data, _keystream(answers, len(data)))).decode("utf-8", errors="replace")
    if not text.startswith("EXPLAIN\n"):
        return
    print()
    print("=" * 60)
    print(text[len("EXPLAIN\n"):].rstrip())
    print("=" * 60)
    print("（もう一度読むには: python quest.py --explain）")


def ask_github_id(progress):
    """GitHub ID を一度だけ聞いて、覚えておく。"""
    if progress.get("github_id"):
        return progress["github_id"]
    print()
    print("フラグは、あなたの GitHub アカウント専用に作られます。")
    while True:
        github_id = input("GitHub ID を入力してください（https://github.com/<ID> の <ID> の部分）: ").strip().lstrip("@")
        if github_id and " " not in github_id:
            break
        print("GitHub ID に空白は入りません。もう一度入力してください。")
    progress["github_id"] = github_id
    save_progress(progress)
    return github_id


def show_flag(quest, progress):
    stages = quest["stages"]
    github_id = ask_github_id(progress)
    flag = make_flag(github_id, [progress[str(i)] for i in range(1, len(stages) + 1)])
    print()
    print(f"{github_id} さんのフラグです:")
    print()
    print(f"    {flag}")
    print()
    print(f"{quest.get('quests_name', '現場')} の Issue の「Submit a Flag」フォームで提出してください:")
    print(f"    {quest.get('submit_url', '（先生に聞いてください）')}")
    print("（GitHub ID をまちがえたときは: python quest.py --id）")


def show_status(quest, progress):
    print(quest["title"])
    for i, _ in enumerate(quest["stages"], start=1):
        mark = "クリア" if str(i) in progress else "まだ"
        print(f"  ステージ {i}: {mark}")


def play_stage(quest, progress, number):
    stages = quest["stages"]
    if not 1 <= number <= len(stages):
        print(f"エラー: ステージ {number} はありません。このクエストのステージは {len(stages)} つです。")
        return 1
    for previous in range(1, number):
        if str(previous) not in progress:
            print(f"エラー: 先にステージ {previous} をクリアしてください。")
            return 1

    stage = stages[number - 1]
    required = stage.get("requires_file")
    if required and not (HERE / required["path"]).exists():
        print("Traceback (most recent call last):")
        print(f'  File "quest.py", line {40 + number}, in <module>')
        print(required["error"])
        return 1

    print(f"== ステージ {number} ==")
    print(stage["question"])
    answer = input("答え: ")
    if sha256(normalize(answer)) != stage["answer_sha256"]:
        print("ちがいます。README と資料をもう一度読んでみましょう。")
        return 1

    progress[str(number)] = normalize(answer)
    save_progress(progress)
    print(f"正解！ ステージ {number} をクリアしました。")

    if all(str(i) in progress for i in range(1, len(stages) + 1)):
        print()
        print("すべてのステージをクリアしました！")
        show_flag(quest, progress)
        show_explanation(quest, progress)
    else:
        print(f"次: python quest.py --stage {number + 1}")
    return 0


def main():
    quest = load_stages()
    parser = argparse.ArgumentParser(
        description=f"{quest['title']}：すべてのステージに答えるとフラグがもらえます。",
        epilog="例: python quest.py --stage 1",
    )
    parser.add_argument("--stage", type=int, metavar="N", help="ステージ N に挑戦する")
    parser.add_argument("--status", action="store_true", help="クリアしたステージを表示する")
    parser.add_argument("--flag", action="store_true", help="フラグをもう一度表示する")
    parser.add_argument("--id", action="store_true", help="GitHub ID を入力し直して、フラグを表示する")
    parser.add_argument("--explain", action="store_true",
                        help="解説を表示する（すべてのステージをクリアした後）")
    parser.add_argument("--reset", action="store_true", help="進み具合を消して、最初からやり直す")
    args = parser.parse_args()

    progress = load_progress()
    if args.flag or args.id:
        if args.id:
            progress.pop("github_id", None)
        if not all(str(i) in progress for i in range(1, len(quest["stages"]) + 1)):
            print("まだクリアしていないステージがあります。確認: python quest.py --status")
            return 1
        show_flag(quest, progress)
        return 0
    if args.explain:
        if not all(str(i) in progress for i in range(1, len(quest["stages"]) + 1)):
            print("解説は、すべてのステージをクリアすると読めます。確認: python quest.py --status")
            return 1
        if not quest.get("explanation"):
            print("このクエストには解説がありません。")
            return 1
        show_explanation(quest, progress)
        return 0
    if args.reset:
        if PROGRESS_FILE.exists():
            PROGRESS_FILE.unlink()
        print("進み具合を消しました。")
        return 0
    if args.status:
        show_status(quest, progress)
        return 0
    if args.stage is None:
        parser.print_help()
        return 0
    return play_stage(quest, progress, args.stage)


if __name__ == "__main__":
    sys.exit(main())
