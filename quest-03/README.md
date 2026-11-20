# Quest 3: The Strict Server

> **このクエストのねらい**
>
> 知らないコマンドの使い方を、help の表示だけで読み解きます。usage の記号の意味、既定値、サブコマンドごとの help を読みます。後半は git のドキュメントで option を調べて、目的のコミットを探します。

サーバールームの前で、運用担当の Daiki が1枚の画面を見せてくれた。Northwind のサーバーを、止めずに動かし続けている人だ。

「これが `nwctl`。うちの管理ツール。……性格は、かなりきつい」

「ツールに性格があるんですか」

「正しく呼ばないと、絶対に動かない。まちがえても、やさしく教えてはくれない。でも、1つだけ律儀でさ。呼び方だけは、聞けば必ず答えるんだ。help って頼めばいい」

このクエストで読むのは **help メッセージ**（英語）です。

コマンドラインのツールには、たいてい help があります。開発者が最初に読むものです。

## 進め方

ツールに話しかけてみます。

    python nwctl.py

それから、ステージに答えます。

    python quest.py --stage 1
    python quest.py --stage 2
    python quest.py --stage 3

`nwctl.py` は何回動かしてもかまいません。

## ファイル

| ファイル | 中身 |
| --- | --- |
| `nwctl.py` | 管理ツール。コマンドラインのツール |
| `history.py` | アプリの履歴を作る（ステージ3） |

`nwctl.py` と `history.py` は編集しないでください。代わりに help を読みましょう。

## help の出し方

たいていのツールは、`--help`（または `-h`）をつけると help を表示します。

    python nwctl.py --help

`git commit` や `git log` のように、**コマンド**（サブコマンドとも言います）を持つツールもあります。
コマンドにはそれぞれの help があり、そこにはもっと多くのオプションが載っていることがよくあります。

    python nwctl.py COMMAND --help

## usage 行の読み方

help は **usage** の行から始まります。コマンドの書き方を示す行です。

    usage: tool.py [-h] [--color {red,blue}] [--fast | --slow] name [name ...]

| 書き方 | 意味 |
| --- | --- |
| `[--fast]` | 省略できる。書かなくてもよい |
| `name`（かっこなし） | 必須。必ず書く |
| `{red,blue}` | このうち1つを選ぶ：`red` か `blue` |
| `name [name ...]` | 1つ以上。いくつでも書ける |
| `--fast \| --slow` | どちらか1つだけ使う。両方は使えない（*mutually exclusive*：互いに排他的） |
| `COMMAND ...` | コマンドと、そのコマンドのオプション |

たとえば、次はどれも正しい書き方です。

    python tool.py Taro
    python tool.py --color red Taro Hanako
    python tool.py --slow Taro

次はまちがいです。`--fast` と `--slow` をいっしょに使っているからです。

    python tool.py --fast --slow Taro

usage 行の下では、オプションを1つずつ説明しています。
`(default: ...)` は、自分で選ばなかったときにツールが使う値です。

## 履歴（ステージ3）

チームは、アプリの履歴を git リポジトリで管理しています。
5人が50個のコミットをしました。コミットには、それぞれ作者（author）とメッセージがあります。

履歴を作ります。

    python history.py --setup

`history` フォルダに移動して、履歴を見てみましょう。

    cd history
    git log

50個のコミットを1つずつ読むのは大変です。
`git log` には、見たいコミットだけを表示するオプションがあります。

`git log -h` が表示するのは、オプションの**短い**一覧です。載っていないオプションもあります。
すべてを見るには、`git log --help` を実行するか、Web のページを読みます（英語）。
https://git-scm.com/docs/git-log

コミットを絞り込むオプションを探しましょう。オプションは、いくつか同時に使えます。

わからなくなったら、もう一度 `python history.py --setup` を実行してください。最初の状態から作り直します。

## 困ったとき

**ツールが `error:` と表示して止まる**

それで正常です。ツールが、呼び方を教えてくれています。
エラーのすぐ上にある usage 行を読みましょう。

**`git log` で探しても、1つも表示されない**

絞り込みのオプションは、ふつう大文字と小文字を区別します（`Backup` と `backup` は別の言葉）。
区別しないようにするオプションもあります。`git log --help` の中を "case" で探してみましょう。

**`git log` の表示が終わらず、入力に戻れない**

git は長い表示を1ページずつ見せます。
`Space` で次のページ、`q` で終了です。

**`git log --help` が "No manual entry" と表示する**

help のページがインストールされていません。
同じページを Web で読みましょう：https://git-scm.com/docs/git-log

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
