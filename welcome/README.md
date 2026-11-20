# 新人のためのクエスト（第14・15回）

来月、Northwind に新しい人が入ってくる。初日のあなたが README を読んで Wi-Fi の合言葉を探したように、
今度は、あなたが案内する番だ。

このフォルダには、みんなが作った「新人のためのクエスト」が入ります。1人1つ、`welcome/YOUR-ID/` に作ります。

## 決まり

- クエストの README（`README.md`）は**英語**で書きます。ひな型は [`_template/README.md`](_template/README.md) です
- 答えは**英語の単語1つ**です。README をよく読めばたどり着けるようにします
- README のほかに、ファイルを1つ以上置きます（メモ、設定ファイル、小さな Python のプログラムなど）。
  答えは、そのファイルを読んだり実行したりして見つかるようにします
- **答えの単語を、そのまま README に書かないでください**
- 本名や、学校・会社の名前は書きません。ここは、だれでも読めます
- 変えてよいのは、自分のフォルダ `welcome/YOUR-ID/` の中だけです

Quest 0 を思い出してみましょう。Prerequisites、Usage、Troubleshooting、Note……。
どの見出しに何を書けば、初めての人が迷わないでしょうか。

## 第14回：作って、遊ぶ

### 前半：作る

1. リポジトリのいちばん上のフォルダで、新しいブランチを作り、ひな型をコピーします。`YOUR-ID` は、あなたの GitHub ID にします。

       git switch main
       git switch -c welcome-quest
       cp -r welcome/_template welcome/YOUR-ID

2. `welcome/YOUR-ID/README.md` の `TODO` を、すべて英語で書きかえます。ほかのファイルも足します。
3. 自分で一度、README だけを見て解いてみます。
4. 自分のフォルダだけをコミットし、push します。

       git add welcome/YOUR-ID
       git commit -m "feat: add a welcome quest by YOUR-ID"
       git push -u origin welcome-quest

5. Quest 14 と同じように、元の現場へプルリクエストを出します。
   この変更には Issue がないので、`Closes #` の行は消してかまいません。
   プルリクエストの自動チェックは、`TODO` が残っていると ❌ になります。書きかえて、同じブランチに push し直しましょう。

前半の終わりに、先生がまとめてマージします。

### 後半：ほかの人のクエストを遊ぶ

1. 自分の fork で **Sync fork** → **Update branch** を押し、codespace で取り込みます。

       git switch main
       git pull

2. 授業で先生が示す組み合わせの表で、だれのクエストを遊ぶかを確かめます。
   そのクエストを、**README だけを頼りに**解きます。作った人に質問してはいけません。
3. 答えがわかったら、作った人に直接伝えます。
4. **Welcome quest feedback** のフォームで、元の現場に Issue を出します。どこで迷ったかを英語で書きます。
   **答えは書きません。**

   https://github.com/kwaka1208/quests-test/issues/new/choose

## 第15回：届いた Issue に答える

1. 元の現場の Issue で、`welcome` のラベルの中から、自分のフォルダについての Issue を探します。
   Issue の一覧にはフラグの提出なども並んでいるので、ラベルで絞り込んだ次の一覧を使います。

   https://github.com/kwaka1208/quests-test/issues?q=is%3Aissue+label%3Awelcome

2. まず、Issue にお礼と、どう直すかを英語でコメントします。
3. README を直し、プルリクエストを出します。説明文には `Closes #N` を書きます。

       git switch main
       git pull
       git switch -c welcome-fix
       （README を直す）
       git add welcome/YOUR-ID
       git commit -m "docs: make the usage of my welcome quest clearer"
       git push -u origin welcome-fix

4. 最後に、15回でできるようになったことを発表します。
