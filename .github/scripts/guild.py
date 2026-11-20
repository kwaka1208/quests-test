"""ルーキークエストテスト bot: checks Join and Flag issues (runs in this repository, the one students fork).

  python3 guild.py process       # (GitHub Actions) check a newly opened issue
  python3 guild.py export OUT    # (teacher) write a CSV of who cleared which quest

All state lives in issues and their labels. Labels are changed only by this script or by the teacher,
so students cannot fake them. There is no leaderboard and there are no points: the record of
correct flags (issues with the `cleared` and `quest-XX` labels) is all we keep.
"""
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO = os.environ.get("GITHUB_REPOSITORY", "")

QUEST_RE = re.compile(r"^quest-\d{2}$")
HANDLE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _-]{0,19}$")

LABEL_COLORS = {
    "join": "0e8a16", "member": "0e8a16", "flag": "1d76db", "cleared": "fbca04",
    "wrong": "d93f0b", "invalid": "cccccc", "rejected": "000000",
}


# ---------- GitHub (through the gh CLI) ----------

def gh(*args, check=True):
    r = subprocess.run(["gh", *args], text=True, capture_output=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {r.stderr.strip()}")
    return r


def list_issues(label):
    """All issues (open and closed) with a label, oldest first."""
    out = gh("api", f"repos/{REPO}/issues?state=all&labels={label}&per_page=100",
             "--paginate", "--slurp").stdout
    pages = json.loads(out) if out.strip() else []
    issues = [i for page in pages for i in page if "pull_request" not in i]
    issues.sort(key=lambda i: i["created_at"])
    return issues


_known_labels = set()


def ensure_label(name):
    if name in _known_labels:
        return
    color = LABEL_COLORS.get(name, "c5def5")
    gh("label", "create", name, "--repo", REPO, "--color", color, "--force")
    _known_labels.add(name)


def reply(number, message, add=(), close=True):
    gh("issue", "comment", str(number), "--repo", REPO, "--body", message)
    for label in add:
        ensure_label(label)
    if add:
        gh("issue", "edit", str(number), "--repo", REPO, "--add-label", ",".join(add))
    if close:
        gh("issue", "close", str(number), "--repo", REPO)


# ---------- helpers ----------

def normalize(answer):
    return " ".join(answer.strip().lower().split())


def make_flag(github_id, answers):
    """Must match engine/quest.py."""
    joined = "|".join(normalize(a) for a in answers)
    digest = hashlib.sha256((github_id.strip().lower() + "|" + joined).encode("utf-8")).hexdigest()
    return "FLAG{" + digest[:10] + "}"


def parse_form(body):
    """Turn an issue form body ('### Label\\n\\nvalue') into {label: value}."""
    fields = {}
    for section in re.split(r"^### ", body or "", flags=re.M)[1:]:
        label, _, value = section.partition("\n")
        value = value.strip()
        fields[label.strip()] = "" if value == "_No response_" else value
    return fields


def roster():
    ids = re.split(r"[\s,]+", os.environ.get("GUILD_ROSTER", "").strip())
    return {i.lower() for i in ids if i}


def quest_answers():
    raw = os.environ.get("QUEST_ANSWERS", "").strip()
    return json.loads(raw) if raw else {}


def parse_time(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


# ---------- reading the state ----------

def gather():
    allowed = roster()

    def ok(login):
        return not allowed or login.lower() in allowed

    members = {}  # login -> {github_id, handle}; the latest Join wins
    for issue in list_issues("member"):
        login = issue["user"]["login"]
        f = parse_form(issue["body"])
        if ok(login):
            members[login.lower()] = {"github_id": login, "handle": f.get("Handle", login)}

    clears = defaultdict(dict)  # login -> {quest: time of the first correct flag}
    for issue in list_issues("cleared"):
        login = issue["user"]["login"].lower()
        for label in issue["labels"]:
            q = label["name"]
            if QUEST_RE.match(q) and q not in clears[login]:
                clears[login][q] = parse_time(issue["created_at"])

    return members, clears


# ---------- process a new issue ----------

def process():
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    issue = event["issue"]
    number = issue["number"]
    login = issue["user"]["login"]
    labels = {l["name"] for l in issue["labels"]}
    fields = parse_form(issue["body"])

    if labels & {"join", "flag"} and roster() and login.lower() not in roster():
        reply(number, f"@{login} さん、ごめんなさい。受講者の名簿にあなたの ID がありません。"
                      "この授業の受講者なら、先生に伝えてください。", ["rejected"])
        return

    if "join" in labels:
        handle = fields.get("Handle", "").strip()
        if not HANDLE_RE.match(handle):
            reply(number, "あと少し！ **Handle** は、英字・数字・空白・`-`・`_` を使って1〜20文字で書いてください。"
                          "直して、新しい Issue を作り直してください。", ["invalid"])
        else:
            reply(number, f"ルーキークエストテスト へようこそ、**{handle}** さん！ 🎉", ["member"])
        return

    if "flag" in labels:
        members, clears = gather()
        if login.lower() not in members:
            reply(number, "先に参加登録をしてください。**Join ルーキークエストテスト** のフォームを使います。", ["invalid"])
            return
        answers = quest_answers()
        quest = fields.get("Quest", "").strip().lower()
        flag = fields.get("Flag", "").strip().strip("`")
        if quest not in answers:
            known = ", ".join(f"`{q}`" for q in sorted(answers)) or "（まだありません）"
            reply(number, f"そのクエストは見つかりません。公開中のクエスト: {known}", ["invalid"])
            return
        if quest in clears.get(login.lower(), {}):
            reply(number, f"`{quest}` はもうクリアしています。🎉 もう一度提出する必要はありません。", ["invalid"])
            return
        if flag == make_flag(login, answers[quest]):
            reply(number, f"✅ 正解！ `{quest}` をクリアしました。おめでとう！", ["cleared", quest])
        else:
            if not (flag.startswith("FLAG{") and flag.endswith("}")):
                tip = "フラグは `FLAG{xxxxxxxxxx}` のような形です。"
            else:
                tip = (f"`quest.py` に GitHub ID（`{login}`）を正しく入力したか、"
                       "フラグを全部写したかを確かめてください。")
            reply(number, f"❌ `{quest}` のフラグがちがいます。{tip} それから、新しい Issue を作り直してください。", ["wrong"])
        return

    # Any other issue (bug reports, team pages, welcome feedback, questions) is left for the teacher.


# ---------- the record of clears ----------

def quest_names_for(clears):
    names = set(quest_answers())
    for c in clears.values():
        names |= set(c)
    return sorted(names)


def export(out_path):
    """One row per member: 1 if the member cleared the quest, else 0, and the number of clears."""
    members, clears = gather()
    names = quest_names_for(clears)
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["github_id", "handle", *names, "cleared"])
        for sid, m in sorted(members.items()):
            done = clears.get(sid, {})
            w.writerow([m["github_id"], m["handle"], *[1 if q in done else 0 for q in names],
                        sum(1 for q in names if q in done)])
    print(f"Wrote {out_path} ({len(members)} members)")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "process":
        process()
    elif command == "export" and len(sys.argv) > 2:
        export(sys.argv[2])
    else:
        sys.exit(__doc__)
