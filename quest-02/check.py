"""エラーメッセージをチェックし、合格したら単語を表示します。

  python check.py --stage 1
  python check.py --stage 2

このチェッカーが確かめられるのは、メッセージの形だけです。中身のよさまではわかりません。
書いたメッセージを声に出して読み、「初めての人の役に立つか？」と自分に聞いてみましょう。
"""
import argparse
import base64
import json
import re
import string
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_LENGTH = 100
KIOSK_PLACEHOLDERS = {"command", "item", "price", "money", "limit"}
COLD_WORDS = ["stupid", "idiot", "dumb", "illegal", "fatal", "invalid", "go away"]
ACTION_WORDS = {"try", "type", "use", "check", "choose", "pick", "enter", "say", "look", "go", "run",
                "press", "add", "open", "ask", "come", "drop", "buy", "sell", "wait", "read", "write",
                "find", "keep", "please", "make", "save", "earn", "get"}

# Which messages each part checks, and which placeholders each message must use.
PARTS = {
    1: {"unknown_command": set(), "unknown_item": set(), "no_money": set()},
    2: {"unknown_command": {"command"}, "unknown_item": {"item"}, "no_money": {"price"}},
}
WORDS = {1: "Y2FsbQ==", 2: "Y29tcGFzcw=="}


def placeholders(message):
    try:
        return {name for _, name, _, _ in string.Formatter().parse(message) if name is not None}
    except ValueError:
        return None


def tone_problems(message):
    """Stage 1 rules: the message is short, calm, and polite."""
    problems = []
    if not message.strip():
        return ["メッセージが空です。書いてください。"]
    if len(message) > MAX_LENGTH:
        problems.append(f"メッセージが長すぎます（{len(message)} 文字）。{MAX_LENGTH} 文字以内にしてください。")
    plain = re.sub(r"\{[^}]*\}", "", message)
    shouting = [w for w in re.findall(r"[A-Za-z]+", plain) if len(w) >= 3 and w.isupper()]
    if shouting:
        problems.append(f"叫ばないでください。'{shouting[0]}' を小文字にするか、消してください。")
    if "!!" in message:
        problems.append("'!' は1つで十分です。使わなくてもかまいません。")
    for word in COLD_WORDS:
        if re.search(r"\b" + word + r"\b", message.lower()):
            problems.append(f"'{word}' は冷たく、失礼に聞こえます。何が起きたかを、ふつうの言葉で書きましょう。")
    return problems


def help_problems(message, required, allowed):
    """Stage 2 rules: the message says what happened and what to do next."""
    problems = []
    names = placeholders(message)
    if names is None:
        return ["'{' か '}' が閉じていません。プレースホルダーは {item} のように書きます。"]
    if allowed is not None:
        for name in sorted(names - allowed):
            problems.append(f"{{{name}}} というプレースホルダーはありません。使えるのは: "
                            + ", ".join("{" + a + "}" for a in sorted(allowed)))
    for name in sorted(required - names):
        problems.append(f"{name} を相手に見せましょう。メッセージに {{{name}}} を入れてください。")
    if message.rstrip()[-1:] not in (".", "!", "?"):
        problems.append("メッセージの最後は '.'、'!'、'?' のどれかにしてください。")
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", message.strip()) if s.strip()]
    if len(sentences) < 2:
        problems.append("短い文を2つ書いてください。「何が起きたか」と「次に何をすればよいか」です。")
    first_words = [re.sub(r"^[^A-Za-z]+", "", s).split(" ")[0].lower() for s in sentences]
    if not any(w in ACTION_WORDS for w in first_words) and "you can" not in message.lower():
        problems.append("次に何をすればよいかを伝えましょう。'Try'、'Type'、'Check' のような動詞で始まる文を書いてください。")
    return problems


def check_messages(messages, rules, allowed, full):
    failed = 0
    for key, required in rules.items():
        message = messages.get(key)
        if not isinstance(message, str):
            print(f"[{key}] がありません。キーを消したり、名前を変えたりしないでください。")
            failed += 1
            continue
        problems = tone_problems(message)
        if full and not problems:
            problems = help_problems(message, required, allowed)
        if problems:
            failed += 1
            print(f"[{key}] {message!r}")
            for p in problems:
                print(f"    - {p}")
        else:
            print(f"[{key}] OK")
    return failed


def load_kiosk_messages():
    try:
        return json.loads((HERE / "messages.json").read_text(encoding="utf-8"))
    except ValueError as err:
        sys.exit(f"messages.json が壊れています: {err}\nQuest 1 と同じように、行（line）と列（column）を読みましょう。")


def main():
    parser = argparse.ArgumentParser(description="エラーメッセージをチェックします。",
                                     epilog="例: python check.py --stage 1")
    parser.add_argument("--stage", dest="part", type=int, choices=[1, 2], required=True, help="チェックするステージの番号")
    args = parser.parse_args()

    failed = check_messages(load_kiosk_messages(), PARTS[args.part], KIOSK_PLACEHOLDERS, args.part >= 2)

    print()
    if failed:
        print("まだです。上の問題を直して、もう一度チェックしてください。")
        return 1
    print(f"ステージ {args.part} 合格！")
    print(f"ステージ {args.part} の答えになる単語: {base64.b64decode(WORDS[args.part]).decode()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
