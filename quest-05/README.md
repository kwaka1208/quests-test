# Quest 5: The Docs Room

> **このクエストのねらい**
>
> Python の公式ドキュメントから、関数が追加されたバージョンを探します。後半はライブラリのドキュメントを読みます。版によって書いてあることが違うので、自分が使っている版に合ったページを読むことを経験します。

廊下のつきあたりに、ドキュメント担当の Haruka の部屋がある。紙の資料とモニターで、壁が見えない。

「探しものなら、ここに全部あるよ」

Haruka は、画面から目を離さずに言った。

「ただし、正しいページにたどり着ければ、の話。開発者って、毎日これをやってるんだ。**公式ドキュメント**を読むってこと」

「全部」の量を見て、少し気が遠くなる。でも、全部を読むわけじゃない。必要な1ページを探せばいい。

このクエストで読むのは **ドキュメント**（英語）です。まず Python 自身のドキュメント、次にライブラリのドキュメントを読みます。

## 進め方

ステージに答えます。

    python quest.py --stage 1
    python quest.py --stage 2
    python quest.py --stage 3

## ファイル

| ファイル | 中身 |
| --- | --- |
| `find_person.py` | Daiki が昔書いたスクリプト。`phonebook` ライブラリを使う（ステージ2・3） |
| `phonebook/` | `phonebook` ライブラリ |
| `docs/` | `phonebook` のドキュメント。`docs/index.md` から読み始める。Web サイトでも読める（下の「ステージ2・3」） |
| `staff.book` | 社員の電話帳 |
| `old.book` | とても古い電話帳 |

`find_person.py` は編集してかまいません。このフォルダに新しいファイルを作ってもかまいません。
`phonebook` ライブラリと電話帳は編集しないでください。

## ステージ1：Python のドキュメント

Python の公式ドキュメントは https://docs.python.org/ にあります（英語。画面の上で日本語に切り替えられますが、このクエストでは英語のまま読みましょう）。
ドキュメントは Python のバージョンごとに分かれています。このクエストでは **Python 3.12** のページを使います（URL の `3.12` の部分がバージョンです）。新しいバージョンでは、ページの場所や書き方が変わることがあります。

とくに役に立つのは、次の2つです。

| ページ | 中身 |
| --- | --- |
| [The Python Standard Library](https://docs.python.org/3.12/library/index.html) | Python についてくるすべてのモジュール（`math`、`random`、`json` など） |
| [Built-in Types](https://docs.python.org/3.12/library/stdtypes.html) | `str`、`list`、`dict` と、そのメソッド |

長いページで何かを探すときは、ブラウザの検索（`Ctrl+F`。Mac は `Cmd+F`）を使いましょう。

### 項目の読み方

関数には、それぞれ次のような**項目（entry）**があります。

> **round(number, ndigits=None)**
>
> Return *number* rounded to *ndigits* precision after the decimal point.
> If *ndigits* is omitted or is `None`, it returns the nearest integer to its input.

- 1行目は **シグネチャ**（signature）です。関数の名前と**引数（parameter）**が書いてあります
- `ndigits=None` は、`ndigits` に既定値があるという意味です。省略できます
- シグネチャの中の `/` は、「これより前の引数は名前で指定できない」という意味です
- 項目の最後に、バージョンについての注記があることがあります

| 注記 | 意味 |
| --- | --- |
| *Added in version X* | バージョン X で追加された。X より前のバージョンにはない |
| *Changed in version X* | バージョン X から動きが変わった |
| *Deprecated since version X* | まだ動くが、いずれ削除される。使うのをやめる |

古いページでは、*Added in version X* の代わりに *New in version X* と書いてあることがあります。意味は同じです。

## ステージ2・3：ライブラリのドキュメント

Daiki は何年も前に `find_person.py` を書きました。今はもう動きません。

    python find_person.py

ライブラリは変わります。新しいバージョンが出ると、名前が変わる関数や、削除される関数があります。
だから、最初に確かめることはいつも同じです。
**自分が使っているのはどのバージョンか。このページはどのバージョンのものか。**

`docs/index.md` を開いて、そこから読み始めましょう。

同じドキュメントは、Northwind の Web サイトでも読めます。中身はフォルダと同じなので、読みやすいほうを使ってください。

https://kwaka1208.github.io/northwind-developers/docs/phonebook/

## 困ったとき

**`ModuleNotFoundError: No module named 'phonebook'` と出る**

`find_person.py` は、このフォルダ（`phonebook` フォルダが入っているフォルダ）で実行してください。

**ドキュメントのページの見た目が、上の例と違う**

それでかまいません。ページのデザインはバージョンによって変わります。
シグネチャとバージョンの注記は、いつも載っています。

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
