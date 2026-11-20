# Quest 6: The Docs Writer

> **このクエストのねらい**
>
> 関数1つの説明ページを、決まった見出しの形で英語で書きます。ページに載せた例が本当に動くことを確かめるところまでが課題です。

ドキュメント室をまたのぞくと、Haruka が小さなメモをひらひらさせていた。

「配送チームが便利なツールを作ったんだけどね。使い方を知ってる人が、誰もいない」

「説明のページは？」

「ない。だから困ってる」

Haruka は、メモをこちらに差し出した。

「ページのないツールは、迷子と同じ。きみが書いてくれないかな」

前のクエストでは、ドキュメントを**読み**ました。

このクエストでは、ドキュメントを英語で**書き**ます。

## 進め方

Python で関数を試してみましょう。

    python
    >>> from delivery import delivery_time
    >>> delivery_time(80)

`delivery_time.md` にページを書いたら、チェックします。

    python check.py --stage 1

ステージの課題に合格すると、チェッカーが単語を1つ表示します。その単語で、同じステージに答えます。

    python quest.py --stage 1

ステージは2つあります。順番に進めてください。

## ファイル

| ファイル | 中身 |
| --- | --- |
| `delivery.py` | 配送チームのツール。関数 `delivery_time()` が1つだけ入っている |
| `memo.md` | 配送チームからのメモ。引数の単位などが書いてある |
| `delivery_time.md` | `delivery_time()` のページ。**このファイルを書きます** |
| `check.py` | ページをチェックし、単語を表示する |

`delivery.py`・`check.py` は編集しないでください。

## よい関数のページには何が書いてあるか

よいページは、初めて使う人の疑問に、次の順で答えます。

1. **何をするのか？**：タイトルの下に1文
2. **何を渡すのか？**：引数（Parameters）
3. **何が返ってくるのか？**：戻り値（Returns）
4. **どう使うのか？**：本当に動く例（Example）

別の関数のページの例です（英語で書きます）。

````markdown
# add_points()

Adds points to a user's score and returns the new total.

## Parameters

- `score` (dict): the user's score. It must have the key `"points"`.
- `amount` (int): how many points to add. Default: `1`.

## Returns

The new number of points in the score (int).

## Example

```python
>>> score = {"points": 10}
>>> add_points(score, 5)
15
>>> add_points(score)
16
```
````

## 例のチェックのしかた

`>>>` で始まる行はコードです。その下の行は、Python が表示する内容です。
チェッカーは、Python に打ち込むのと同じように、あなたの例を実行します。
これを **doctest** と呼びます。Python だけで実行できます（`doctest` モジュール）。

ですから、出力を想像で書いてはいけません。**コードを実行して、Python が表示したものを写してください。**
`3` と `3.0` は違います！

## ステージ1：要約・引数・戻り値

`delivery_time.md` を開きます。タイトルと3つの見出しは、もう書いてあります。

- タイトルの下の `TODO` を、1文に置き換えます。大文字で始め、`.` で終わる文です
- `delivery.py` と `memo.md` を読んで `delivery_time()` の引数と単位を確かめ、関数を試してみましょう。
  `## Parameters` の下に、上の例のように、引数**1つごとに**リストの項目を1つ書きます。
  既定値のある引数には、`Default: ...` と既定値を書きます
- `## Returns` の下に、関数が何を返すかを書きます

書きたければ、`## Raises` のような別の節を足してもかまいません。

    python check.py --stage 1

## ステージ2：動く例

`## Example` の下に、コードブロックで例を**2つ以上**書きます。
役に立つ例を見せましょう。たとえば、距離だけを渡す呼び出しと、ほかの引数も渡す呼び出しです。

    python check.py --stage 2

## 困ったとき

**「ページの記述: … Python の出力: …」と出る**

例を Python で実行し、出力をそのまま写してください。空白も確かめましょう。

**わざとエラーになる例を書きたい**

かまいません。`Traceback (most recent call last):` から始まるエラー全体を写してください。

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
