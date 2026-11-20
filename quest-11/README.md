# Quest 11: The Code Notes

> **このクエストのねらい**
>
> コードに書かれた英語（docstring とコメント）を読みます。docstring の Args・Returns から正しい呼び方を読み取り、`deprecated`・`TODO`・`FIXME` の意味を知ります。最後は、コメントとコードが食い違うときにコードを確かめることを経験します。

朝会。Haruto がホワイトボードに大きく書いた。**Northwind Lunch v2.0**。

「来月リリースする。全員に担当を振るよ」

ペンの先が、こちらを向いた。

「きみはランチのポイント。そう、あの『ポイントの謎』のコードだ。古いけど、メモはたくさん残ってる」

責任重大だ。席に戻ると、Misaki が小声で言った。

「コードはコンピューターのために書く。でもメモは、人のために書くんだよ。よく読んで。ただし、メモがいつも最新とは限らない」

このクエストで読むのは **docstring** と **コメント**（英語）です。コードの中にある英語です。

## 進め方

`lunch_points.py` を読み、3つのチェック用スクリプトを直して、実行します。

    python price_check.py
    python bonus_check.py
    python order_check.py

うまく動くと、スクリプトが単語を表示します。その単語でステージに答えます。

    python quest.py --stage 1
    python quest.py --stage 2
    python quest.py --stage 3

## ファイル

| ファイル | 中身 |
| --- | --- |
| `lunch_points.py` | ランチのポイントの古いコード。読むだけで、編集しない |
| `price_check.py` | ステージ1 |
| `bonus_check.py` | ステージ2 |
| `order_check.py` | ステージ3 |

チェック用スクリプトで編集してよいのは、`Edit this line` の下の行だけです。

## docstring の読み方

**docstring** は、`def` のすぐ下の `"""` で囲まれた文です。関数の使い方を教えてくれます。
多くのプロジェクトでは、次のように書きます（Google スタイル）。

    def points_for(price):
        """Return the points for one lunch.        <- 何をするか（1行）

        Args:                                      <- 何を渡すか
            price (float): The price in dollars.   <- 名前 (型): 意味

        Returns:                                   <- 何が返ってくるか
            int: The points.

        Raises:                                    <- 起こしうるエラー
            ValueError: If price is negative.
        """

ファイルを開かなくても、docstring を読めます。

    python -m pydoc lunch_points

`Space` で次のページ、`q` で終了です。

## コメントのメモ

**コメント**は `#` で始まります。開発者は、コメントで特別な言葉を使います。

| 言葉 | 意味 |
| --- | --- |
| `NOTE:` | 大事な情報。読むこと |
| `TODO:` | まだ終わっていない作業 |
| `FIXME:` | わかっているバグ。直す必要がある |
| `deprecated` | 古い。新しいコードでは使わない。ふつうは代わりに何を使うかも書いてある |

## コメントとコードが食い違うとき

コメントは、コンピューターがチェックしてくれません。誰かがコードを変えたとき、
コメントを直し忘れることがあります。するとコメントがまちがいになります。

## 困ったとき

**`DeprecationWarning` と出る**

古いものを使っている、と Python が警告しています。その行の続きを読みましょう。代わりに何を使えばよいか書いてあることが多いです。

**`NameError: name '...' is not defined` と出る**

関数の名前のつづりを確かめてください。`lunch_points.py` から写しましょう。

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
