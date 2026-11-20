# Quest 19: The Release Desk

> **このクエストのねらい**
>
> リリースノート（CHANGELOG）を読みます。Added・Changed・Deprecated・Removed の違いと、版番号（semver）の意味を知り、古い起動方法と設定を新しい版に合わせます。`DeprecationWarning` は移行ガイドを読んで消します。

**今日は Northwind Lunch v2.0 のリリース日だ！**

……のはずが、朝からキッチンがざわついている。

v2.0 には、注文を大きな画面に出すツール **kitchen-display 3.0** が必要だ。Daiki が今朝それを更新して、いつもどおりに起動した。

    python display.py --fullscreen

動かない。

「勘でいじらないで」Haruka が止めた。「ツールが変わったなら、何が変わったかは **CHANGELOG** に書いてある。3.0 で使えなくなったものもあるし、まだ使えるけど、もうすぐ消えるものもある」

このクエストで読むのは **CHANGELOG**（変更履歴）と **移行ガイド**（英語）です。

## 進め方

ツールを動かして、何と言うか読みます。

    python display.py --fullscreen

起動のしかた（ステージ1）を直し、次に `display.json`（ステージ2・3）を直します。
1つ直すたびに、ツールが合言葉（code word）を表示します。その単語でステージに答えます。

    python quest.py --stage 1
    python quest.py --stage 2
    python quest.py --stage 3

## ファイル

| ファイル | 中身 |
| --- | --- |
| `CHANGELOG.md` | kitchen-display のリリースノート |
| `MIGRATION.md` | 2.x から 3.0 に移るためのガイド |
| `display.json` | 設定。2.1 向けに書かれている。**このファイルを直します** |
| `display.py` | kitchen-display 3.0.0。編集しない |

## CHANGELOG の読み方

いちばん新しいバージョンが上にあります。バージョンごとに、次の節があります。

| 節 | 意味 |
| --- | --- |
| Added | 新しい機能 |
| Changed | 動きが変わったもの |
| Deprecated | まだ動くが、いずれ削除される。早めに使うのをやめる |
| Removed | もうない |
| Fixed | バグの修正 |
| **BREAKING** | 古いコマンドや設定が動かなくなるかもしれない。よく読むこと！ |

先に "Deprecated" になり、もっと新しいバージョンで "Removed" になります。
よい CHANGELOG には、代わりに**何を使えばよいか**も書いてあります。

## バージョン番号（semver）

    3 . 0 . 0
    |   |   +-- PATCH：バグの修正だけ
    |   +------ MINOR：新しい機能。古いものもそのまま動く
    +---------- MAJOR：互換性のない変更。古いものが動かなくなるかもしれない

ですから、最初の数字が上がったとき（2.x → 3.0）は、更新する前に CHANGELOG を読みましょう。

## 警告とエラー

- **エラー**はプログラムを止めます。すぐに直す必要があります
- **警告**（`DeprecationWarning` など）はプログラムを止めません。今日は動きますが、いずれ動かなくなります。
  動かなくなる前に直しましょう

## 困ったとき

**`display.json is broken` と出る**

カンマと引用符を確かめてください。JSON の文字列は `"..."` で囲みます。`true` と数は囲みません。

**`display.json` を壊してしまい、最初からやり直したい**

このフォルダで `git restore display.json` を実行します。

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
