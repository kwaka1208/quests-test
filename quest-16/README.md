# Quest 16: Sprint Review II

> **このクエストのねらい**
>
> 中間のまとめ（書き）です。第1〜8回で書いたもの（エラーメッセージ、help、バグ報告、コミットメッセージ）を、もう一度、自分の力で書きます。

ベータ版のトラブルは、なんとか片づいた。——と思ったら、Haruto の話には続きがあった。

「明日までに、きれいにしておきたい。サーバーは人に怒鳴るし、help は空っぽだ。それと Kaito が、さっきもう1つバグを見つけた。ちゃんと直せるように、報告を書いてほしい」

長い夜になりそうだ。

## 進め方

ステージは2つあります。順番に進めてください。制限時間は先生が伝えます。

    python check.py --stage 1
    python quest.py --stage 1

## ファイル

| ファイル | ステージ | 中身 |
| --- | --- | --- |
| `server.py` | 1 | ベータ版のサーバー。**`ERRORS` と help の文を編集します** |
| `night.py` | 2 | 今夜の予約注文を数える。バグがある。編集しない |
| `orders.json`、`late.json` | 2 | 予約注文のファイルが2つ（`late.json` は、夜おそくに届いた予約） |
| `bug-report.md` | 2 | **ここにバグ報告を書きます** |
| `commit.txt` | 2 | **ここに、修正のコミットメッセージを書きます** |
| `check.py` | すべて | 作業をチェックし、単語を表示する |

## ステージ1：優しいエラーと、わかりやすい help

`server.py` で、次のことをします。

- `ERRORS` の2つのメッセージを書き直す（Quest 2）：落ち着いた、短い2文（何が起きたか、次に何をすればよいか）。
  プレースホルダー `{env}` か `{port}` を使う
- 2つの help の文を書く（Quest 4）：小文字で始め、最後にピリオドをつけず、`%(default)s` を使う

試してみましょう。

    python server.py
    python server.py --env test
    python server.py --help

それからチェックします。

    python check.py --stage 1

## ステージ2：バグ報告とコミットメッセージ

`night.py` は `orders.json` では動きますが、`late.json` では動きません。両方試してみましょう。2つのファイルの中身も見比べて、何が違うのかを確かめてから報告を書きます。

    python night.py orders.json
    python night.py late.json

- `bug-report.md` にバグ報告を書く（Quest 8）：タイトル、コマンドをバッククォートで囲んだ番号つきの手順、
  Expected、Actual（実際のエラーの最後の行）、Environment（Python のバージョン）
- `commit.txt` に、この修正のコミットメッセージの1行目を書く：`type: subject`

それからチェックします。

    python check.py --stage 2

## 困ったとき

**`server.py がエラーで止まります` と出る**

引用符とカンマを確かめてください。help の文に `%` を1つだけ書くと壊れます。`%%` と書きます。

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
