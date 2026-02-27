---
title: "HTML・CSS知識不要！Antigravityでブログカスタマイズを爆速化する方法"
slug: "2026-02-19"
date: 2026-02-19T08:00:00Z
lastmod: 2026-02-19T12:11:25.825Z
draft: false
tags: ["AI"]
categories: []
image: "/images/img_421bf202699a.png"
---

<article>
<div class="separator" style="clear: both; text-align: center;"><a href="/images/img_cc5916a395bd.jpg" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1536" data-original-width="2816" height="350" src="/images/img_421bf202699a.png" width="640" /></a></div><br />こんにちは、てつです！
<p>2月も後半に入り、少しずつ春の気配を感じるようになってきましたね。みなさんいかがお過ごしでしょうか？</p>
<p>さて、みなさんはブログ書いてますか？</p>
<p>Googleがリリースした新しいコードエディタ<b>「Antigravity（アンチグラビティ）」</b>をご存知でしょうか？ 直訳すると<b>「反重力」</b>。名前がもう中二病心をくすぐりますが（笑）、これがブログ運営やWebデザインにおいて、まさに重力から解放されたような軽快さをもたらしてくれるんです。</p>
<p>今回は、この謎めいたツール<b>「Antigravity」</b>を使って、ブログのデザイン調整や記事作成を効率化する方法を備忘録としてまとめてみました。<b>「AIエディタって難しそう…」</b>と思っている方にこそ、ぜひ読んでいただきたいです！</p><span></span>

  
## そもそも「Antigravity」って何？

<p>簡単に言うと、Googleが作った<b>「AIエージェントが主役のコードエディタ」</b>です。ベースはみんな大好きVS Codeなんですが、中身は別物。</p>
<p>これまでのAIエディタ（Cursorとか）は「人間が書くのをAIが手伝う」感じでしたが、Antigravityは「人間が指示を出して、AI（Gemini 3 Proなど）が勝手に作業計画を立てて実行する」という、もう一段階上の自動化を実現しています。</p>

  
### ここがポイント！

<p>「ヘッダーの色を変えて」と頼むと、CSSファイルを探して、該当箇所を修正して、プレビューまで勝手にやってくれるイメージです。まさに「監督」になる感じ！</p>

  
## 活用法①：面倒な「表作成」を一瞬で終わらせる

<p>ブログを書いていると、「比較表」を作りたくなることありますよね。でも、HTMLでtableタグを書いて、CSSで装飾して…って正直めんどくさい。</p>
<p>そんな時こそAntigravityの出番です。実はこれ、画像をドラッグ＆ドロップして「これと同じ表を作って」と言うだけでコードを書いてくれるんです。「え、そんなのアリ？」って思いますよね。</p>

  
### 実践：AffinityとAdobeの比較表を作ってみた

<p>例えば、こんなスクショがあったとします。「Affinityの新プランとAdobe CCの比較」です。これを手打ちするのは大変ですよね。</p>
<p>そこで、Antigravityに画像を投げてこう指示しました。</p>

<blockquote style="background-color: #282a36; border-left: 5px solid rgb(255, 121, 198); border-radius: 4px; color: #f8f8f2; font-family: Consolas, monospace; padding: 15px;">
<p style="color: #8be9fd; margin-top: 0px; text-align: center;"><strong>プロンプト：</strong></p>
<p style="margin-bottom: 0px; text-align: left;">この画像を読み取って、見やすいHTMLのテーブルを作成して。デザインはダークモード風で、Affinityの「0円」の部分は赤文字で強調。</p>
</blockquote>

<p>すると、AIエージェントが数秒で以下のようなコードとプレビューを生成してくれました！</p>

<table border="1" style="background-color: #222222; border-collapse: collapse; color: #eeeeee; text-align: left; width: 100%;">
<thead>
<tr style="background-color: #444444;">
<th style="border: 1px solid rgb(85, 85, 85); padding: 10px;">機能</th>
<th style="border: 1px solid rgb(85, 85, 85); padding: 10px;">Affinity (新プラン)</th>
<th style="border: 1px solid rgb(85, 85, 85); padding: 10px;">Adobe CC</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid rgb(85, 85, 85); padding: 10px;">編集ツール<br /><small>(ブラシ、ペン、レイヤー等)</small></td>
<td style="border: 1px solid rgb(85, 85, 85); padding: 10px;"><span style="color: #ff6b6b; font-weight: bold;">0円 (無料)</span></td>
<td style="border: 1px solid rgb(85, 85, 85); padding: 10px;">月額サブスクリプション</td>
</tr>
<tr>
<td style="border: 1px solid rgb(85, 85, 85); padding: 10px;">保存・書き出し</td>
<td style="border: 1px solid rgb(85, 85, 85); padding: 10px;"><span style="color: #ff6b6b; font-weight: bold;">0円 (無料)</span></td>
<td style="border: 1px solid rgb(85, 85, 85); padding: 10px;">月額サブスクリプション</td>
</tr>
<tr>
<td style="border: 1px solid rgb(85, 85, 85); padding: 10px;">AI機能<br /><small>(生成塗りつぶし等)</small></td>
<td style="border: 1px solid rgb(85, 85, 85); padding: 10px;">有料<br /><small>(Canva Pro契約が必要)</small></td>
<td style="border: 1px solid rgb(85, 85, 85); padding: 10px;">プランに含まれる<br /><small>(クレジット制限あり)</small></td>
</tr>
</tbody>
</table>

<p>すごくないですか？ セルの結合や補足テキスト（カッコ内の文字）まで完璧に認識しています。これをコピペするだけで記事のパーツが完成です。</p>

  
## 活用法②：サイトデザインの微調整

<p>ブログのデザインを変えたい時も便利です。「記事の文字サイズを少し大きくして」「見出しのデザインを吹き出し風にして」とチャットで伝えると、実際のプレビュー画面を見ながらAIがCSSをいじってくれます。</p>
<p>特にAntigravityは「ブラウザ操作」もできるので、実際にブラウザでどう表示されるかを確認しながらテストしてくれるのが強み。</p>

  
### 実践：ページ送りボタンの配置変更

<p>実際に私がやってみて感動したのが、ページ下部のナビゲーション（ページ送り）の修正です。</p>
<p>ブログテンプレートの初期状態だと、ただ「その他の投稿」というリンクが表示されているだけで、ちょっと不親切だったんですよね。</p>
<p>そこで、Antigravity上でその部分を指し示して、こんな風に頼んでみました。</p>

<blockquote style="background-color: #282a36; border-left: 5px solid rgb(255, 121, 198); border-radius: 4px; color: #f8f8f2; font-family: Consolas, monospace; padding: 15px;">
<p style="color: #8be9fd; margin-top: 0px; text-align: center;"><strong>プロンプト：</strong></p>
<p style="margin-bottom: 0px; text-align: left;">この「その他の投稿」という部分を修正したい。「&lt; 前のページ」と「次のページ &gt;」という2つのリンクに変更して、画面の左右の端に配置。<span style="background-color: transparent;">&nbsp;</span></p></blockquote>

<p>すると、AIがHTML構造とCSSを解析して、サクッと修正してくれました。</p>

<div class="separator" style="clear: both; text-align: center;"><a href="/images/img_5a0c684948ae.jpg" style="margin-left: 1em; margin-right: 1em;"><img data-original-height="164" data-original-width="1179" height="90" src="/images/img_8034acef41bb.jpg" width="640" /></a></div><div class="separator" style="clear: both; text-align: center;"><a href="/images/img_a25a5e31fb46.jpg" style="margin-left: 1em; margin-right: 1em;"><img data-original-height="156" data-original-width="1187" height="84" src="/images/img_bf4d5755b004.jpg" width="640" /></a></div><br /><br /><br />CSSのFlexboxを使って「左寄せ」と「右寄せ」にする記述、私で書くと地味に面倒なんですが、AIなら「左右に配置して」の一言で通じます。この直感的な操作感はクセになりますね。

  
### 実践：トップページと2ページ目で「表示記事数」を変える

<p>もう一つ、Bloggerを使っている人にしか伝わらないかもしれない（笑）、地味だけど重要な調整を行いました。</p>
<p>私のブログでは、「トップページは10記事表示したいけど、2ページ目以降はデザインの都合上9記事にしたい（3×3で綺麗に並べたい）」というこだわりがありました。</p>
<p>しかし、Bloggerの標準設定で「投稿数」を変更すると、全ページ一律で変わってしまいます。トップページに合わせると2ページ目が崩れるし、その逆もまた然り…。これ、地味にストレスだったんです。</p>

<blockquote style="background-color: #282a36; border-left: 5px solid rgb(255, 121, 198); border-radius: 4px; color: #f8f8f2; font-family: Consolas, monospace; padding: 15px;">
<p style="color: #8be9fd; margin-top: 0px; text-align: center;"><strong>ここでのAIへの無茶振り：</strong></p>
<p style="margin-bottom: 0px; text-align: left;">「トップページは10件のままでいいんだけど、『次のページ』ボタンを押した時だけ、表示件数を9件になるようにリンクを調整できない？」</p>
</blockquote>

<p>これに対してもAntigravityは即答。「JavaScriptでページ送りリンクのURLパラメータを書き換えましょう」と提案してくれました。</p>
<p>具体的には、ページ移動のリンクに自動的に <code>max-results=9</code> というパラメータを付与する処理を実装してくれたんです。おかげで、メインページは10件、検索結果や2ページ目以降は9件という、理想の挙動が実現しました。</p>
<p>本来ならJavaScriptをごりごり書かないといけない場面ですが、これも「やりたいこと」を伝えただけでコードを生成されたので、本当に楽でした。</p>

  
## 活用法③：ブログカードを「私好み」に刷新

<p>ブログにとって、「リンクカード（ブログカード）」のデザインは記事の印象を決める重要な要素です。</p>
<p>私はこれまで「はてなブログカード」を使っていましたが、iframeで読み込むためデザインのカスタマイズができませんでした。「もっとこう、画像が左にあって、タイトルが右にある、シンプルで見やすいデザインにしたい…」と思っていました。</p>
<p>そこでAntigravityに「この画像（理想のデザイン）と同じにして！」と、完成イメージの画像を投げつけてみました。</p>
  
<blockquote style="background-color: #282a36; border-left: 5px solid rgb(255, 121, 198); border-radius: 4px; color: #f8f8f2; font-family: Consolas, monospace; padding: 15px;">
<p style="color: #8be9fd; margin-top: 0px; text-align: center;"><strong>プロンプト：</strong></p>
<p style="margin-bottom: 0px; text-align: left;">「現在のブログカードデザインを添付した画像のようにして」</p>
</blockquote>

<p>すると、AIエージェントは驚くべき対応をしました。</p>
<p>これまでは外部サービス（はてなブログパーツ）の枠をただ表示していただけだったのを、「APIから記事のメタデータ（タイトルや画像）を取得して、私でHTMLを組み立てる」というJavaScriptのプログラムに丸ごと書き換えてくれたのです。</p><p>以前のブログカードデザイン</p><div class="separator" style="clear: both; text-align: center;"><a href="/images/img_84e757322a69.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="250" data-original-width="859" height="186" src="/images/img_0a5c775e6661.png" width="640" /></a></div><p>変更後のデザイン</p><p><a href="https://antigravity.google/">https://antigravity.google/</a></p>
<p>途中で「表示が遅い」という問題が発生したときも、「データ取得APIをより高速なものに変更しましょう」と提案してくれ、最終的に読み込み速度もデザインも完璧なものが出来上がりました。</p>
<p>しかも、「データ取得に失敗したら、元のはてなカードを表示する」という安全装置（フォールバック）まで実装済み。まさにプロの仕事です。</p><p>下記記事で、追記として変更後コードを追加しました。</p><p><a href="https://tetsu-miscellaneous.blogspot.com/2026/02/bloggerurlok.html">https://tetsu-miscellaneous.blogspot.com/2026/02/bloggerurlok.html</a></p>


  
## まとめ：重力から解放されよう

<p>「Antigravity」は、単なるコードエディタというより、「超優秀なアシスタントがついた作業部屋」という感じです。</p>
<p>ブログの記事執筆（特に面倒なHTMLコーディング）や、サイトのちょっとしたデザイン修正にかかる時間が劇的に減ります。今はまだプレビュー版で無料で触れるようなので、今のうちにこの「未来の作業感」を体験しておくのがおすすめですよ！</p>
<p>みなさんも、AIツールを使って「楽」できるところはどんどん楽していきましょう。それでは、また！</p>
</article>





