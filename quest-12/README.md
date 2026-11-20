# Quest 12: The Docstring Desk

> **このクエストのねらい**
>
> 関数の docstring を英語で書きます。1行目は動詞の原形で始める短い要約にし、Args・Returns・Raises を実際のコードに合わせて書きます。

古いポイントのコードは、なんとか読めるようになった。すると Misaki が、別のファイルを開いた。`menu.py`。

「この関数、ちゃんと動く。でも見て」

スクロールしても、docstring が1つもない。

「先週、docstring に助けられたよね。今度は助ける側。次にこれを読む人のために、書いてあげて」

前のクエストでは、docstring とコメントを**読み**ました。このクエストでは、docstring を英語で**書き**ます。

## 進め方

`menu.py` の関数を見て、試してみましょう。

    python
    >>> from menu import total_price, find_item, print_menu
    >>> total_price(["salad", "coffee"])
    >>> find_item("Salad")
    >>> print_menu()

`menu.py` に docstring を書いたら、チェックします。

    python check.py --stage 1

ステージの課題に合格すると、チェッカーが単語を1つ表示します。その単語で、同じステージに答えます。

    python quest.py --stage 1

ステージは2つあります。順番に進めてください。

## ファイル

| ファイル | 中身 |
| --- | --- |
| `menu.py` | Northwind Lunch のメニュー。**ここに docstring を書きます** |
| `check.py` | docstring をチェックし、単語を表示する |

`menu.py` には docstring だけを書き足してください。コードは変えないでください。`check.py` は編集しないでください。

## docstring の書き方

`def` の行のすぐ下に、`"""` で囲んで書きます。どの行も、先頭に空白を4つ入れます。

    def add_points(score, amount=1):
        """Add points to a score and return the new total.

        Args:
            score (dict): The user's score. It must have the key "points".
            amount (int): How many points to add. Default is 1.

        Returns:
            int: The new number of points.

        Raises:
            KeyError: If score has no key "points".
        """

### 1行目

- 短い1文。最後は `.`
- 命令文のように、**原形**の動詞で始める：`Return`、`Add`、`Show`、`Find`。
  `Returns` や `Returned`、`This function returns` ではありません
- その後ろに空の行を1行入れる

### 節（セクション）

| 節 | 書くとき | 書き方 |
| --- | --- | --- |
| `Args:` | 関数に引数があるとき | 引数**1つごとに**1行：`name (type): what it is.` |
| `Returns:` | 関数が値を返すとき | `type: what it is.` |
| `Raises:` | 関数がエラーを起こすことがあるとき | `ErrorName: when it happens.` |

書くのは、その関数に必要な節だけです。
表示するだけで何も返さない関数には、`Returns:` の節はいりません。

## ステージ1：1行目

3つの関数それぞれに、1行目だけの docstring を書きます。

    python check.py --stage 1

## ステージ2：Args・Returns・Raises

それぞれの関数に必要な節を書き足します。コードをよく読みましょう。

- どんな引数があるか？
- 値を返すか？
- エラーを `raise` するか？

      python check.py --stage 2

## 困ったとき

**`IndentationError` と出る**

docstring の行の先頭には、関数の中のコードと同じ数の空白（ふつうは4つ）が必要です。

**チェッカーが「動詞は原形にしてください」と言う**

動詞は命令文の形で書きます。`Returns the price.` ではなく `Return the price.` です。

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
