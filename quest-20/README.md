# Quest 20: The Release Notes

> **このクエストのねらい**
>
> コミットの一覧から、リリースノート（CHANGELOG）を英語で書きます。使う人に関係のある変更だけを選び、Keep a Changelog の見出しに分けます。互換性がなくなる変更には BREAKING と書き、最後に貢献者として自分の名前を載せます。

Northwind Lunch v2.0 は、準備完了。最後の仕事を持ってきたのは、Haruka だった。

「2.0.0 のリリースノート、書いてくれない？ 1.5.0 から後のコミットは、全部ここにある」

画面には、コミットの一覧。

「でも利用者は、コミットを1つずつ読みたいわけじゃない。知りたいのは3つだけ。何が新しくなったか、何が直ったか、自分は何を変えなきゃいけないか。それと、もう1つ」

Haruka が、ファイルのいちばん下を指さした。**Contributors**（貢献者）。

「ここに、きみの名前も入る。ポイントを直したのは、きみだから」

前のクエストでは、リリースノートを**読み**ました。このクエストでは、リリースノートを英語で**書き**ます。

## 進め方

`commits.txt` を読みます。`CHANGELOG.md` の 2.0.0 の部分を書いたら、チェックします。

    python check.py --stage 1

ステージの課題に合格すると、チェッカーが単語を1つ表示します。その単語で、同じステージに答えます。

    python quest.py --stage 1

ステージは2つあります。順番に進めてください。

## ファイル

| ファイル | 中身 |
| --- | --- |
| `commits.txt` | 1.5.0 から 2.0.0 までのコミット |
| `CHANGELOG.md` | リリースノート。**このファイルを編集します** |
| `check.py` | CHANGELOG をチェックし、単語を表示する |

## コミットから CHANGELOG へ

| コミットの type | 書く場所 | 理由 |
| --- | --- | --- |
| `feat:` | `### Added` | 新しい機能 |
| `fix:` | `### Fixed` | バグの修正 |
| `feat!:` や `fix!:`（`!` つき） | `### Changed` か `### Removed`。**BREAKING** をつける | 古いコードや設定が動かなくなる |
| （あとで削除されるもの） | `### Deprecated` | まだ動くが、使うのをやめてほしい |
| `docs:`、`refactor:`、`test:`、`chore:` | （CHANGELOG には書かない） | 利用者には見えない変更 |

1行1行は、開発者ではなく**利用者**に向けて書きます。利用者にとって何が変わったかを書きましょう。

| よくない | よい |
| --- | --- |
| `fix: round half up when giving points` | `Points are rounded half up. A 5-dollar lunch now gives 3 points.` |
| `feat!: rename the setting pickup` | `**BREAKING:** The setting pickup is renamed to pickup_time.` |

バージョンの見出しには、バージョンと日付（YYYY-MM-DD）を書きます。

    ## [2.0.0] - 2026-12-01

## ステージ1：Added と Fixed

`TODO` と `YYYY-MM-DD` を置き換えます。利用者に見えるコミットについて、`### Added` と `### Fixed` を書きます。
利用者に見えないコミットのことは書きません。

    python check.py --stage 1

## ステージ2：互換性のない変更・非推奨・貢献者

- 互換性のない変更（`!` つき）2つを、`### Changed` と `### Removed` に、**BREAKING** をつけて書く
- `points_rate` について `### Deprecated` を書く。代わりに何を使うかも書く
- ファイルの最後に `## Contributors` を足す。コミットした人**全員**（`docs` や `test` のコミットの人も）と、
  **あなた**を書く。GitHub ID に `@` をつけて書き、`@YOU` の代わりにあなた自身の ID を書く

あなたの GitHub ID を指定して、チェックします。

    python check.py --stage 2 YOUR-ID

## 困ったとき

**「日付は … YYYY-MM-DD の形で書いてください」と出る**

たとえば `2026-12-01` です。年は4けた、月は2けた、日は2けたで書きます。

**「… のことは書かないでください」と出る**

そのコミットは `docs`・`refactor`・`test` のどれかです。利用者には見えないので、CHANGELOG には書きません。
（でも、それを作った人は、ちゃんと貢献者です！）

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
