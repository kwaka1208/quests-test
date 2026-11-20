# Quest 0: The First Day

> **このクエストのねらい**
>
> README を頭から全部読むのではなく、見出しを手がかりに必要な情報を探す練習です。途中でエラーが出たときも README を頼りに自分で解決し、古い情報と今の情報を見分けることを経験します。

## このクエストの進め方

初出社の朝。小さなソフトウェア会社 **Northwind** のドアを開けたとたん、最初の壁にぶつかった。

受付の貼り紙に、こう書いてある。

「オフィスの Wi-Fi を使えるのは、**README を読める人**だけです」

……試されてる？ 初日から？

固まっていると、通りがかった先輩エンジニアが笑った。

「大丈夫。みんな最初はここからだから」

このページの線から下が、このクエストの **README（英語）** です。

全部を頭から読む必要はありません。まず見出しを見て、必要な節を探しましょう。

進め方も、困ったときの対処も、この README の中に書いてあります。

---

## Prerequisites

- Python 3.10 or later
- GitHub Codespaces (see "Getting started" in the top README of this repository)

To check your Python version, run:

    python --version

## Installation

There is nothing to install.

## Usage

This quest has three stages. Run them in order:

    python quest.py --stage 1
    python quest.py --stage 2
    python quest.py --stage 3

Each stage asks you one question. The answer is somewhere in this repository.

To see which stages you have cleared, run:

    python quest.py --status

> **Note:** The answer to stage 3 is **not** in this file.
> Open `docs/ARCHIVE.md` and look for the heading that begins with **"Deprecated"**.
> Read carefully: old information is not always current information.

When you clear all three stages, you will get a flag.
Submit it in **ルーキークエストテスト** with the **Submit a Flag** issue form.

## Troubleshooting

**`BadgeError: the visitor badge is missing`**

You need a visitor badge. Create an empty file named `visitor.badge` in this folder,
and run the stage again.
You do not need to write anything in the file.

**I typed a wrong answer**

That is OK. Run the same stage again.

## Maintainers

This quest is maintained by **Misaki**, a senior engineer at Northwind.
If you find a bug in this quest, please open an issue.
See [CONTRIBUTING.md](../CONTRIBUTING.md) to learn how.

## License

This quest is released under the MIT License. See [LICENSE](../LICENSE).
