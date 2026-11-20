# Quest 15: Sprint Review I

> **このクエストのねらい**
>
> 中間のまとめ（読み）です。第2〜8回で読んだ英文（エラーメッセージ、help、ドキュメント、Q&A、Issue、コードコメント、Pull Request）を、組み合わせて使います。教室では時間を区切って取り組みます。

**v2.0 ベータ版**の公開前夜。静かだったオフィスで、最初のアラートが鳴った。

ベータ版のサーバーが起動しない。メニューが同期しない。「値段がおかしい」という問い合わせまで来た。

全部、同時に。

Haruto が立ち上がる。「残り1時間。1つずつ片づけよう」

Misaki と目が合った。

「エラーメッセージ、help、ドキュメント、Issue、プルリクエスト。全部読んできたよね。今夜は、その全部を使う」

## 進め方

問題は3つあります。1つが1ステージです。

    python quest.py --stage 1
    python quest.py --stage 2
    python quest.py --stage 3

制限時間は先生が伝えます。

## ファイル

| ファイル | ステージ | 中身 |
| --- | --- | --- |
| `beta.py` | 1 | ベータ版のサーバーを起動する。編集しない |
| `beta.json`、`staging.json` | 1 | サーバーの設定 |
| `menu_sync.py` | 2 | メニューを同期する。**このファイルを直します** |
| `kitchen/` | 2 | `kitchen` ライブラリ。編集しない |
| `docs/` | 2 | `kitchen` のドキュメント。Web サイトでも読める（https://kwaka1208.github.io/northwind-developers/docs/kitchen/） |
| `forum/` | 2 | Northwind Answers の質問。Web サイトでも読める（https://kwaka1208.github.io/northwind-developers/answers/） |
| `issues/` | 3 | Issue が3つ |
| `pr-61.md`、`pr-61.diff` | 3 | マージ済みのプルリクエスト |
| `prices.py` | 3 | 値段。**このファイルを直します** |
| `total.py` | 3 | 合計の値段を表示する。編集しない |

## 思い出そう

どうすればよいかは、これまでのクエストで学んでいます。困ったら、そのクエストを思い出しましょう。

| こんなときは… | 思い出すクエスト |
| --- | --- |
| Traceback が出た | 1 |
| 行番号つきの JSON のエラーが出た | 1 |
| `error: the following arguments are required` と出た | 3 |
| 古いコードが動かない | 5 |
| 長い Issue | 7 |
| Q&A のページに回答がたくさんある | 9 |
| コメントとコードが食い違う | 11 |
| プルリクエスト | 13 |

## 困ったとき

**行き詰まった**

エラーメッセージを、最後の行から、ゆっくりもう一度読みましょう。それでもだめなら、ヒントカードをもらいましょう。

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
