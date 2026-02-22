---
title: "【Gmail整理術】大切なメール（★）だけ残して、古い通知は自動でポイ！"
slug: "2026-02-16"
date: 2026-02-16T10:11:00Z
lastmod: 2026-02-16T10:11:33.503Z
draft: false
tags: []
categories: []
image: "/images/img_9d3d739fa36e.jpg"
---

<div class="separator" style="clear: both; text-align: center;"><a href="/images/img_02f15dfde47a.jpg" style="margin-left: 1em; margin-right: 1em;"><img data-original-height="559" data-original-width="1024" height="350" src="/images/img_9d3d739fa36e.jpg" width="640" /></a></div><br />Gmailを長く使っていると、メルマガや通知メールが溜まりに溜まって「保存容量が少なくなっています」という警告が出ること、ありませんか？

<p>毎回手動で検索して削除するのは非常に面倒です。そこで今回は、<strong>「3ヶ月以上前のメールを自動でゴミ箱に移動する（ただしスター付きの大事なメールは残す）」</strong>という、一度設定すれば完全放置できる便利な自動化テクニックをご紹介します。</p>

<p>難しい知識は一切不要です。この記事の通りに「コピー＆ペースト」するだけで、誰でも5分で設定できますよ！</p>


## 用意するもの：Google Apps Script（GAS）


<p>今回は、Googleが無料で提供している「Google Apps Script（通称：GAS）」というツールを使います。難しそうに聞こえますが、簡単なので安心してください。</p>


## ステップ1：プログラムをコピペする


<p>まずは、自動削除の指令を書く画面を開きます。</p>

<ol>
<li>パソコンのブラウザで <a href="https://script.google.com/" rel="noopener" target="_blank">Google Apps Script</a> にアクセスします（Gmailと同じアカウントでログインしてください）。</li>
<li>左上の <strong>「新しいプロジェクト」</strong> をクリックします。</li>
<li>最初から入力されている文字（<code>function myFunction() { ... }</code>）をすべて消します。</li>
<li>代わりに、以下のコードをそのままコピーして貼り付けます。</li>
</ol>

<pre><code>
function Gmail_cleanUp() {
  // 3ヶ月以上前、かつスターがついていないメールを検索
  var searchTerm = 'older_than:3m -is:starred';
  
  // 検索条件に合うメールを取得
  var threads = GmailApp.search(searchTerm);
  
  // 取得したメールをすべてゴミ箱へ移動
  for (var i = 0; i &lt; threads.length; i++) {
    threads[i].moveToTrash();
  }
}
</code></pre>

<ol start="5">
<li>画面左上の「無題のプロジェクト」をクリックし、「Gmail自動クリーンアップ」など分かりやすい名前に変更します。</li>
<li>画面上部にある <strong>「フロッピーディスクのアイコン（プロジェクトを保存）」</strong> をクリックします。</li></ol>


## ステップ2：最初の1回だけ「許可」を出す（※重要）


<p>自分が作ったプログラムを動かすために、Googleに「自分のGmailを操作していいよ」という許可を出します。初めての時は少し怖い画面が出ますが、落ち着いて進めましょう。</p>

<ol>
<li>画面上部の <strong>「▷ 実行」</strong> ボタンをクリックします。</li>
<li>「承認が必要です」というポップアップが出たら <strong>「権限を確認」</strong> をクリックします。</li>
<li>自分のGoogleアカウントを選択します。</li>
<li><strong>「このアプリは Google で確認されていません」</strong> という警告画面が出ます。（※自分が作ったプログラムなので表示されるだけです。安心してください）</li>
<li>左下の <strong>「詳細」</strong> をクリックし、一番下に出てくる <strong>「Gmail自動クリーンアップ（安全ではないページ）に移動」</strong> をクリックします。</li>
<li>次の画面で右下の <strong>「許可」</strong> をクリックします。</li>
</ol>

<p>これで下準備は完了です！</p>


## ステップ3：毎日自動で動くようにタイマーをセットする


<div class="separator" style="clear: both; text-align: center;"><a href="/images/img_e94f501ed940.jpg" style="margin-left: 1em; margin-right: 1em;"><img data-original-height="1024" data-original-width="1024" height="640" src="/images/img_643a88d6d98d.jpg" width="640" /></a></div><br />最後に、このプログラムが「毎日勝手に」動くようにタイマー（トリガー）をセットします。

<ol>
<li>画面左側のメニューから、<strong>「時計のアイコン（トリガー）」</strong> をクリックします。</li>
<li>右下の <strong>「＋ トリガーを追加」</strong> をクリックします。</li>
<li>設定画面が開くので、以下のように変更します。
<ul>
<li>実行する関数を選択：<code>Gmail_cleanUp</code></li>
<li>イベントのソースを選択：<strong>時間主導型</strong></li>
<li>時間ベースのトリガーのタイプを選択：<strong>日付ベースのタイマー</strong></li>
<li>時刻を選択：<strong>午前0時～午前1時</strong> （邪魔にならない深夜がおすすめです）</li>
</ul>
</li>
<li>右下の <strong>「保存」</strong> をクリックします。</li>
</ol>

<p>お疲れ様でした！これで全ての設定が完了です。</p>


## まとめと注意点


<p>設定が完了すると、毎日指定した時間に自動で古いメールがゴミ箱に移動していきます。</p>

<ul>
<li><strong>いきなり完全消去はされません</strong><br />メールは一旦「ゴミ箱」に入ります。Googleの仕様により、ゴミ箱に入ったメールは30日後に完全に削除されます。万が一必要なメールが消えても、30日以内なら救出できるので安心です。</li>
<li><strong>溜まりすぎている場合は数日かかります</strong><br />システムの仕様上、1回の自動実行で処理できるのは最大500件程度です。もし古いメールが何万件も溜まっている場合は、1日500件ずつ毎日少しずつゴミ箱へ移動し、徐々に綺麗になっていきます。</li>
</ul>


### 【応用】削除する期間を変更したい場合は？


<p>今回のコードでは「3ヶ月前」に設定していますが、プログラムの中の<strong>英数字を1文字変えるだけ</strong>で、好きな期間に変更できます。</p>

<p>ステップ1で貼り付けたコードの3行目にある、以下の部分に注目してください。</p>

<pre><code>var searchTerm = 'older_than:3m -is:starred';</code></pre>

<p>この <code>3m</code> という部分が期間を表しています。「m」は「month（月）」のことです。<br />ここを以下のように書き換えるだけで、自分の好きな期間にカスタマイズできますよ！</p>

<ul>
<li><strong>1ヶ月前</strong>のメールを消したい場合：<code>older_than:1m</code> に変更</li>
<li><strong>半年（6ヶ月）前</strong>のメールを消したい場合：<code>older_than:6m</code> に変更</li>
<li><strong>1年前</strong>のメールを消したい場合：<code>older_than:1y</code> に変更（「y」はyearの頭文字です）</li>
<li><strong>14日前</strong>のメールを消したい場合：<code>older_than:14d</code> に変更（「d」はdayの頭文字です）</li>
</ul>

<p>ご自身のメールの溜まり具合に合わせて、ぜひお好みの期間で設定してみてくださいね！</p>