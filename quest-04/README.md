# Quest 4: The Clear Help

> **このクエストのねらい**
>
> 前回は help を読む側でしたが、今回は書く側に回ります。argparse の慣習に沿って help テキストを英語で書き、既定値の表示とツールの説明も添えます。

翌日。Daiki が、ちょっと得意げにノート PC を回してきた。

「昨日の夜、作った。日報を出すツール `report.py`。ちゃんと動くよ」

言われるままに `python report.py --help` を打つ。オプションは並んでいる。でも、説明が1語もない。

「……これ、どう使うんですか」

「だよね」Daiki は苦笑いした。「help がないツールは、作った本人しか使えない。きみ、`nwctl` の help を読んだだろ。いい help がどんなものか、もうわかるはず。書いてくれない？」

前のクエストでは、help メッセージを**読み**ました。

このクエストでは、help メッセージを英語で**書き**ます。

## 進め方

ツールを動かして、help を見てみましょう。

    python report.py sales
    python report.py --help

`report.py` に help の文を書いたら、チェックします。

    python check.py --stage 1

ステージの課題に合格すると、チェッカーが単語を1つ表示します。その単語で、同じステージに答えます。

    python quest.py --stage 1

ステージは2つあります。順番に進めてください。

## ファイル

| ファイル | 中身 |
| --- | --- |
| `report.py` | 日報ツール。**`build_parser()` の中の help の文を編集します** |
| `check.py` | help の文をチェックし、単語を表示する |

`report.py` で編集するのは、`help=""` と `description=""` の中の文だけです。
名前・既定値・ほかのコードは変えないでください。`check.py` は編集しないでください。

## help の文の書き方

オプションの help には、**そのオプションが何をするか**、または**利用者が何を指定するか**を書きます。
コマンドラインのツールでは、ふつう次のように書きます。

1. **小文字で始める**：`Show more days` ではなく `show more days`
   （`RGB` や `UTC` のような略語は大文字でかまいません）
2. **最後に `.` をつけない**
3. **短く書く**：1行、60文字以内
4. **名前をくり返すだけにしない**：`--days` の help が `days` では、何も伝わりません。
   `how many days the report covers` のほうがよい help です

比べてみましょう。

| 役に立たない | 役に立つ |
| --- | --- |
| `help="Speed."` | `help="how fast the server answers, in seconds"` |
| `help="the color option"` | `help="color of the text on the screen"` |

## 既定値を表示する

多くのオプションには **既定値（default）** があります。利用者が値を選ばなかったときに、ツールが使う値です。
既定値を手で書いてはいけません。あとで誰かが既定値を変えると、help がまちがいになるからです。
`%(default)s` と書きます。argparse が、そこに本当の値を入れてくれます。

    parser.add_argument("--limit", type=int, default=30,
                        help="how many rows to show (default: %(default)s)")

`--help` の表示はこうなります。

      --limit LIMIT  how many rows to show (default: 30)

`%` にはこの特別な意味があるので、`%` を1つだけ書くと help が壊れます。
`%` の記号そのものを表示したいときは、`%%` と書きます。

    help="stop when the disk is more than 90%% full"

## description

**description** は help のいちばん上に表示される文です。ツール全体が何をするかを1文で書きます。
オプションの help と違って、ふつうの文として書きます。大文字で始め、`.` で終わります。

    description="Check the status of the Northwind servers."

## ステージ1：空の help を埋める

ツールの引数（argument）は、どれも help が空です：`help=""`
1つずつ help の文を書いてください。help は想像で書かず、**ツールを動かして確かめてから**書きましょう。
何も表示されないように見えるオプションは、ほかのオプション（たとえば `--save`）と組み合わせて試すと、役目がわかります。
試しに作ったファイル（`--save` で保存したものなど）は、消してかまいません。

    python check.py --stage 1

## ステージ2：既定値と description

既定値のあるオプションがいくつかあります。`%(default)s` で表示してください。
それから `description` を1文で書きます。
チェッカーは、`--help` がきちんと動くかも確かめます。

    python check.py --stage 2

## 困ったとき

**`report.py の … 行目に文法エラーがあります` と出る**

書いた文のまわりの引用符とカンマを確かめてください。文の最初と最後に `"` が1つずつ必要です。

**`badly formed help string` や `--help がエラーで止まります` と出る**

help の文に `%` を1つだけ書いています。`%%` にしてください。`%(default)s` はそのままでかまいません。

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
