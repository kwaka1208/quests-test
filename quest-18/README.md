# Quest 18: The Reviewer

> **このクエストのねらい**
>
> コードレビューを英語で書きます。行番号とラベル（`blocking:`・`nit:`・`question:`・`optional:`）を付け、相手ではなくコードについて、ていねいに書きます。本当のバグだけを blocking にし、レビューの結論をそろえます。最後は、班の人が現場に出した PR に、本物のレビューを付けます。

通知が1件。Daiki が **Pull Request #66** を出した。キッチンの在庫を管理する機能だ。

レビュー担当の欄に、自分の名前がある。

「初レビューだね！」Misaki がうれしそうに言う。「自分がコメントをもらったとき、どう感じたか思い出して。やさしく、わかりやすく。それぞれのコメントがどれくらい大事かも伝えること。それと——本物の問題を、ちゃんと見つけること」

前のクエストでは、コードレビューを**読み**ました。このクエストでは、コードレビューを英語で**書き**ます。

## 進め方

プルリクエストを読み、コードを試します。

    python try_stock.py

`review.md` にレビューを書いたら、チェックします。

    python check.py --stage 1

ステージの課題に合格すると、チェッカーが単語を1つ表示します。その単語で、同じステージに答えます。

    python quest.py --stage 1

ステージは3つあります。順番に進めてください。

## ファイル

| ファイル | 中身 |
| --- | --- |
| `pr-66.md` | プルリクエストの説明文 |
| `stock.py` | プルリクエストのコード。編集しない |
| `try_stock.py` | コードを試す |
| `review.md` | **あなたのレビュー。このファイルを編集します** |
| `check.py` | レビューをチェックし、単語を表示する |

## review.md の書き方

    Decision: Request changes

    - line 8: blocking: You cannot take the last item. This should be ... so that ...
    - line 15: nit: The names k and v are short. Could you use item and count?
    - line 16: question: Do we need ... ?

- 1行目は判断です：`Approve`、`Comment`、`Request changes` のどれか（Quest 17）
- コメントは1行に1つ：`- line 行番号: ラベル: コメント`
- ラベルは Quest 17 と同じ：`blocking:`、`nit:`、`question:`、`optional:`

## 優しく、わかりやすいコメントを書く

| 優しくない | 優しく、わかりやすい |
| --- | --- |
| `This is wrong!!` | `blocking: This returns False when n is 10. It should be >= so that ...` |
| `Bad names.` | `nit: Could you use item instead of k? It is easier to read.` |
| `Why did you do this?` | `question: What happens when the stock is 0?` |

- 人ではなく、**コード**について書く
- **何が**問題で、**何を**すればよいかを書く。`should`、`could you`、`please` が便利です
- どれくらい大事かを、ラベルではっきりさせる
- よいところも伝える！（`Nice!`、`Thanks for this.`）。ラベルの後ろに書きます：`nit: Nice page! Could you ...`

## ステージ1：レビューを書く

判断と、3つ以上のコメントを書きます。質問（`?` つき）を1つ入れてください。

    python check.py --stage 1

## ステージ2：本物のバグを見つける

`pr-66.md` の説明文をもう一度読みましょう。"You can take all the items, down to zero." とあります。
本当でしょうか？ `python try_stock.py` を実行します。バグのある行を見つけて、`blocking:` をつけてください。
blocking にするのは、本物のバグだけです。判断も見直しましょう。

    python check.py --stage 2

## ステージ3：班の人のプルリクエストをレビューする

いよいよ本番だ。第8回に、班のみんなが現場にチームのページのプルリクエストを出した。どれも、まだマージされていない。

「今日は、それをおたがいにレビューする」Misaki が言う。「レビューが終わったら、マージしてもらえる。チームに入る最後の一歩だね」

1. 授業で先生が示す組み合わせの表で、あなたがレビューするプルリクエストの番号を確かめます。
   自分のプルリクエストは、レビューできません。
2. 元の現場の **Pull requests** のタブで、相手のプルリクエストを開きます。
   番号（`#12` など）を覚えておきましょう。
3. **Files changed** のタブを押します。行の横の **+** を押して、ラベルつきのコメントを書き、**Start a review** を押します。
   コメントは2つ以上書きます。英文のまちがい、わかりにくいところ、もっと知りたいことなどです。
   本名や、学校・会社の名前が書いてあったら、それは `blocking:` です。
4. **Review changes**（または **Finish your review**）を押し、**Approve**・**Comment**・**Request changes** のどれかを選んで、
   **Submit review** を押します。
5. このクエストのフォルダでチェックします。レビューしたプルリクエストの番号を指定します。

       python check.py --stage 3 12

あなたのプルリクエストにレビューが届いたら、読んでみましょう。直すところがあれば、
codespace のリポジトリのいちばん上のフォルダで、次のように直します。

    git switch team-page
    （team/YOUR-ID.md を直して保存する）
    git add team/YOUR-ID.md
    git commit -m "docs: fix my team page"
    git push
    git switch main

`team-page` のブランチに push すると、プルリクエストは自動で新しくなります。
最後の `git switch main` を忘れないでください（クエストは main のブランチにあります）。
レビューが終わったプルリクエストは、先生がマージします。

## 困ったとき

**「これは本当にバグですか？」と出る**

名前や書き方の好みは、バグではありません。`nit:` か `optional:` を使いましょう。

**「… さんのレビューが見つかりません」と出る**

**Submit review** を押しましたか？ 送信していないレビューのコメントは、ほかの人には見えません。

## メンテナー

このクエストのメンテナーは **Misaki** です。
クエストのバグを見つけたら、Issue で知らせてください。
やり方は [CONTRIBUTING.md](../CONTRIBUTING.md)（英語）にあります。

## ライセンス

このクエストは MIT ライセンスで公開しています。[LICENSE](../LICENSE) を見てください。
