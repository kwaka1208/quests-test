# Quest 14: The Proposal

> **このクエストのねらい**
>
> Pull Request のタイトルと説明文を英語で書きます。タイトルは `type: subject` の形にし、説明文には Summary・Changes・How to test と `Closes #N` を書きます。Changes には diff にあるものだけを、もれなく書きます。最後は、現場に本物の PR を出します。

「ポイントの謎」を覚えているだろうか。5ドルのランチで、2ポイントしかもらえない件だ。

Kaito が **Issue #52** を立て、修正は自分に回ってきた。コードは直した。diff もできている。あとは——。

「じゃあ、提案しよう」Misaki が言う。「プルリクエストを出すんだよ。この前、読む側をやったでしょ。レビューする人がどこを見るか、もう知ってるはず。自分が読みたくなるようなのを書いて」

前のクエストでは、プルリクエストを**読み**ました。このクエストでは、プルリクエストを英語で**書き**ます。

## 進め方

Issue と、あなたの変更を読みます。

- `issue-52.md`：Issue
- `change.diff`：あなたの変更

`pr.md` に、プルリクエストのタイトルと説明文を書いたら、チェックします。

    python check.py --stage 1

ステージの課題に合格すると、チェッカーが単語を1つ表示します。その単語で、同じステージに答えます。

    python quest.py --stage 1

ステージは3つあります。順番に進めてください。

## ファイル

| ファイル | 中身 |
| --- | --- |
| `issue-52.md` | あなたの変更が直す Issue |
| `change.diff` | あなたの変更 |
| `pr.md` | プルリクエストのタイトルと説明文。**このファイルを編集します** |
| `check.py` | プルリクエストをチェックし、単語を表示する |
| `team-page.md` | チームのページのひな型（ステージ3） |

ほかのファイルは編集しないでください。

## タイトル

プルリクエストのタイトルは、コミットメッセージと同じ決まりで書きます。

    type: subject

| type | 使うとき |
| --- | --- |
| `feat` | 新しい機能 |
| `fix` | バグの修正 |
| `docs` | ドキュメントだけの変更 |
| `refactor` | 動きを変えずに、コードを整理する |
| `test` | テストだけの変更 |

- subject は小文字で始め、**原形**の動詞で始めます：`fix`、`add`、`round`
- 最後にピリオドをつけません。短く書きます（72文字以内）

## 説明文

説明文は、次の形で英語で書きます。

    ## Summary

    What you changed and why, in one or two sentences.

    Closes #52

    ## Changes

    - `file.py`: what changed in this file.

    ## How to test

    1. Run ...
    2. Check that ...

- **Summary**：何をなぜ変えたかを1〜2文で
- `Closes #52` は Issue をつなげます。プルリクエストがマージされると、Issue #52 が自動で閉じます
- **Changes** には、diff にあるファイルを全部書きます。diff にないファイルは書きません。
  （Quest 13 を思い出しましょう。レビューする人は、ここを確かめます！）
- **How to test** には、レビューする人がたどれる手順を書きます

## ステージ1：タイトル

`pr.md` の1行目、`# ` の後ろにタイトルを書きます。

    python check.py --stage 1

## ステージ2：説明文

3つの節を書きます。`change.diff` をよく読みましょう。変わったファイルはどれですか？

    python check.py --stage 2

## ステージ3：チームのページ

練習はここまで。Misaki が、現場のリポジトリを開いた。

「ここに `team` ってフォルダを作るんだ。Northwind では、新しく入った人が、自分のページを1つ足すことになってる。もちろん、プルリクエストでね」

「……本物の、ですか」

「本物の。来週、班の人がレビューする。マージはそのあと」

このステージは、いつもの codespace（現場の fork）だけで進めます。
プルリクエストは、**あなたの fork から、元の現場（upstream）へ**出します。

1. 元の現場に、Issue を立てます。次のページを開き、**Team page** の **Get started** を押します。

   https://github.com/kwaka1208/quests-test/issues/new/choose

   タイトルの最後に、あなたの GitHub ID を足して、**Submit new issue** を押します。
   Issue の番号（`#12` など）を覚えておきましょう。

2. 新しいブランチを作ります。リポジトリのいちばん上のフォルダで実行します。

       cd ..
       git switch -c team-page

3. ひな型をコピーして、あなたのページを作ります。`YOUR-ID` は、あなたの GitHub ID にします。

       mkdir -p team
       cp quest-14/team-page.md team/YOUR-ID.md

   `team/YOUR-ID.md` を開き、`TODO` をすべて英語で書きかえます。1行目は `# YOUR-ID` です。
   **本名や、学校・会社の名前は書かないでください。** このページは、だれでも読めます。

4. そのファイルだけをコミットし、ブランチを push します。

       git add team/YOUR-ID.md
       git commit -m "docs: add a team page for YOUR-ID"
       git push -u origin team-page

   `git add` には、必ずこのファイルの名前を書きます。`git add .` にすると、クエストで編集したファイルまで入ってしまいます。

5. GitHub で**あなたの fork** を開き、**Compare & pull request** を押します。
   `base repository` が元の現場になっていることを確かめます。
   説明文の欄には、Summary・Changes・How to test の見出しがすでに入っています。
   ステージ1・2 の決まりで、タイトルと説明文を書きます。`Closes #` の後ろには、手順 1 の Issue の番号を書きます。
   `<!--` で始まる案内のコメントは消してください（残っていても、チェッカーは読み飛ばします）。
   **Create pull request** を押します。

6. `main` に戻り、チェックします。チェッカーは、あなたが現場に出した、いちばん新しいプルリクエストを読みます。

       git switch main
       cd quest-14
       python check.py --stage 3

**マージはしません。** 第10回に、班の人がこのプルリクエストをレビューします。マージは、そのあとで先生がします。
マージされると、Issue は自動で閉じます。

## 困ったとき

**`… のプルリクエストが見つかりません` と出る**

**Create pull request** まで押しましたか？ GitHub のページが少し遅れることもあります。1分待ってから、もう一度試してください。

**"Compare & pull request" のボタンが見当たらない**

あなたの fork の **Pull requests** のタブを開き、**New pull request** を押します。
`base repository` を元の現場に、`compare:` をあなたのブランチ（`team-page`）にします。

**「変えるのは team/… の1つだけにしてください」と出る**

ほかのファイルまでコミットしています。`git add .` を使いませんでしたか？ 先生に相談してください。
タイトルや説明文だけを直すときは、GitHub でプルリクエストを開き、**Edit** で直してから、もう一度チェックします。

**フォルダの場所がわからなくなった**

`pwd` で、いまいるフォルダがわかります。クエストのフォルダ（`quest-14`）から1つ上が、リポジトリのいちばん上です。

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
