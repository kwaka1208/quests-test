# ルーキークエストテスト

開発の現場では、毎日たくさんの文書を読み、書いています。README、エラーメッセージ、`--help` の表示、Issue、プルリクエストの説明。どれも、エンジニアが仕事で使う大事な文書です。

ここでは、それをゲームのように体験します。あなたは架空のソフトウェア会社 **Northwind** の新入社員です。先輩に案内されながら、会社の仕事を**クエスト**として1つずつ片づけていきます。

ここは、その**現場**です。毎回、新しいクエストのフォルダ（`quest-00/`、`quest-01/`、…）がこのリポジトリに届きます。参加登録も、クエストを終えたしるし（フラグ）の提出も、このリポジトリの **Issue** で行います。

クエストで読む文書は英語です。進め方の説明は日本語で書いてあります。

> **このリポジトリは公開されています。** 本名、学校や会社の名前、そのほか個人的なことは絶対に書かないでください。名前はハンドルネームを使います。

## クエスト

クエストには2つの種類があります。

- **読むクエスト**：現場の文書を読んで、答えを探します。全部を訳す必要はありません。見出しを見て、必要なところを探して読みます
- **書くクエスト**：会社の仕事として、文書を英語で書きます。読む人に伝わるかどうかを、チェックのプログラムが確かめます

どちらも、すべてのステージに答えると**フラグ**（`FLAG{...}` の形の文字列）がもらえます。フラグが、クエストを終えたしるしです。あなたの GitHub ID から作られるので、ほかの人のフラグを写しても通りません。

クエストを進めながら、fork、Issue、プルリクエストなど、オープンソースの開発と同じやり方も覚えていきます。

## 進め方

1. **参加登録**：Issue の **Join ルーキークエストテスト** で参加登録をする（下の「はじめに：参加登録」）
2. **自分の作業場所を作る**：このリポジトリを fork し、Codespaces で開く（下の「はじめに：fork と Codespaces」）
3. **クエストを解く**：クエストのフォルダの README を読み、`quest.py` の問いに答えてフラグを手に入れる
4. **フラグを届ける**：Issue の **Submit a Flag** でフラグを提出する。正解すると記録に残る

3〜4 を、クエストのたびにくり返します。

## はじめに：参加登録

参加登録もフラグの提出も、**Issue** のフォームで行います。フォームに書いて送ると、bot が数秒で返信します。

1. このリポジトリの [New issue](https://github.com/kwaka1208/quests-test/issues/new/choose) を開き、**Join ルーキークエストテスト** を選びます。
2. ハンドルネームを書いて送ります。
3. 数秒待つと、bot が Issue に返信します。登録できたら、`member` のラベルが付きます。

## はじめに：fork と Codespaces

クエストは、このリポジトリの**自分用のコピー**（*fork* と呼びます）で解きます。
**GitHub Codespaces** を使います。Python と git がすぐ使える、ブラウザの中のコンピューターです。

1. このページの右上の **Fork** を押し、**Create fork** を押します。
2. **自分の fork** で、**Code** → **Codespaces** → **Create codespace on main** を押します。
   ブラウザの中で VS Code が開きます。ターミナルは下にあります。
3. 作業が終わったら、codespace を止めます。自分の fork で **Code** → **Codespaces** →
   **...** → **Stop codespace** を押します。アカウントには毎月の無料の時間があり、動いている codespace はその時間を使います。
   次からは、同じメニューから同じ codespace を開きます。

> **メモ：** Issue（参加登録・フラグの提出・バグの報告）は、自分の fork ではなく、**このリポジトリ**（`kwaka1208/quests-test`）に出します。fork では、Issue は最初から使えないようになっています。

## 毎回の授業の前に：新しいクエストを受け取る

新しいクエストは、元のリポジトリ（*upstream* と呼びます。今見ているこのリポジトリです）に追加されます。
それを自分の fork に取り込みます。

1. GitHub で自分の fork を開き、**Sync fork** → **Update branch** を押します。
2. codespace のターミナルで、次を実行します。

       git pull

> **メモ：** ファイルを変更したせいで `git pull` が失敗したときは、`git stash` を実行してから、もう一度試してください。

## クエストの遊び方

はじめての人は、まず [introduction.md](introduction.md) を読んでください。クエストの舞台と、Quest 0 までのいきさつが書いてあります。

1. codespace のターミナルで、クエストのフォルダに移動します。たとえば次のようにします。

       cd quest-00

   フォルダが見つからないときは、上の「毎回の授業の前に」を見てください。

2. クエストの `README.md` を読みます。
3. `quest.py` を実行して、すべてのステージに答えます。最後にフラグがもらえます。

       FLAG{xxxxxxxxxx}

4. このリポジトリの [New issue](https://github.com/kwaka1208/quests-test/issues/new/choose) で **Submit a Flag** のフォームを選び、フラグを提出します。

## フラグの記録

正解したフラグは、Issue に `cleared` のラベルが付いて残ります。これが、あなたの進み具合の記録です。
自分の記録は、[自分がクリアした Issue の一覧](https://github.com/kwaka1208/quests-test/issues?q=is%3Aissue+author%3A%40me+label%3Acleared) で見られます。
順位や点数はありません。ほかの人と競うのではなく、自分のペースで進めましょう。

このリポジトリの Issue には、フラグの提出のほかに、バグの報告やチームのページの依頼なども届きます。探したいものは、ラベルで絞り込めます。

| 探したいもの | 一覧 |
|---|---|
| 自分がクリアしたクエスト | [`cleared`](https://github.com/kwaka1208/quests-test/issues?q=is%3Aissue+author%3A%40me+label%3Acleared) |
| チームのページの依頼（Quest 14） | [`team-page`](https://github.com/kwaka1208/quests-test/issues?q=is%3Aissue+label%3Ateam-page) |
| 新人のためのクエストの感想（第14・15回） | [`welcome`](https://github.com/kwaka1208/quests-test/issues?q=is%3Aissue+label%3Awelcome) |
| 参加登録とフラグの提出を除いたもの | [Issue の一覧](https://github.com/kwaka1208/quests-test/issues?q=is%3Aissue+-label%3Ajoin+-label%3Aflag) |

## チームのページと、新人のためのクエスト

このリポジトリには、クエストのほかに、みんなで作るフォルダが2つあります。

- [`team/`](team/README.md)：チームのページ。Quest 14 で、自分のページをプルリクエストで足します
- [`welcome/`](welcome/README.md)：来月入ってくる新人のためのクエスト。第14・15回に、1人1つ作ります

## ファイルを壊してしまったら

クエストでは、いくつかのファイルを変更します。ファイルを壊してしまい、最初からやり直したいときは、元に戻せます。

    git restore quest-00/README.md

パスは、戻したいファイルのものにしてください。**そのファイルへの変更は消えます。** やり直したいときだけ使いましょう。
どのファイルを変更したかは、`git status` でわかります。

## オープンソース

これは**オープンソースのプロジェクト**でもあります。誰でも貢献できます。

- 問題を見つけたら：[Issue を出す](https://github.com/kwaka1208/quests-test/issues/new/choose)（**Bug report**）
- 自分で直したいときは：[CONTRIBUTING.md](CONTRIBUTING.md)（英語）を読む
- 取り組むものを探しているときは：
  [`good first issue`](https://github.com/kwaka1208/quests-test/labels/good%20first%20issue) のラベルがついた Issue を見る

慣れてきたら、実在のオープンソースにも挑戦してみましょう！ プルリクエストを送る**前に**、
先生に見てもらってください。

## ライセンス

[MIT](LICENSE)
