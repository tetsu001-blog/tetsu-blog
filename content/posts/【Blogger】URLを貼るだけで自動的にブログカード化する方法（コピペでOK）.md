---
title: "【Blogger】URLを貼るだけで自動的にブログカード化する方法（コピペでOK）"
slug: "2026-02-03"
date: 2026-02-03T08:00:00Z
lastmod: 2026-02-19T11:26:59.325Z
draft: false
tags: ["雑記", "デジタル"]
categories: []
image: "/images/img_06c18ab94cd6.jpg"
---

<article>

<div class="separator" style="clear: both; text-align: center;"><a href="/images/img_90270ba3107f.jpg" style="margin-left: 1em; margin-right: 1em;"><img data-original-height="572" data-original-width="1024" height="358" src="/images/img_06c18ab94cd6.jpg" width="640" /></a></div><br />Bloggerで記事を書いていると、「他サイトのリンクを貼るとき、もっと見栄え良くしたい」と思うことはありませんか？
    WordPressなどではURLを貼るだけで自動的に「ブログカード（サムネイル付きのリンクボックス）」が表示されますが、Bloggerの標準機能では単なるテキストリンクになってしまいます。ブログを運営して半年ほどずっと悩んでいました。


<p>調べると手動で、カードを作成する方法はありました。</p>

<p>ですが、毎回手動でカードを作成するツールを使うのも手間なので、<b>「URLを貼るだけで、勝手にブログカードに変換してくれる」</b>カスタマイズを導入してみました。</p>

<p>今回はその方法をシェアします。JavaScript（スクリプト）をテーマに追加するだけで、過去の記事も含めて一括で適用できるので便利です。</p>

<p>※お使いのテーマによっては機能しない可能性もあります。</p>
<br />

    
## このカスタマイズでできること

<p>記事の投稿画面で、以下のように<b>「URLのリンクだけ」</b>を1行に書き上部のリンク挿入をすると</p>

<p style="text-align: center;">https://tetsu-miscellaneous.blogspot.com/</p>

<p>読者が見る画面では、自動的に以下のような<b>ブログカード</b>に変換されて表示されるようになります。</p>

<div class="separator" style="clear: both; text-align: center;"><a href="/images/img_6c860edc8598.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="250" data-original-width="859" height="186" src="/images/img_0c5b2201a24c.png" width="640" /></a></div>


<p>※2026/02/19 ブログカードデザインを変更したため、現在ブログで表示されるデザインは違います。<br />

</p><p>現在のブログカードデザイン</p><p><a href="https://tetsu-miscellaneous.blogspot.com/2026/02/htmlcssantigravity.html">https://tetsu-miscellaneous.blogspot.com/2026/02/htmlcssantigravity.html</a></p>
## 導入手順

<p>作業はBloggerのテーマ（HTML）にコードを追記するだけです。</p>
<p>※念のため、作業前にテーマのバックアップ（XMLのダウンロード）を取っておくことをおすすめします。</p>

<ol>
<li>Blogger管理画面のメニューから<b>「テーマ」</b>をクリック</li>
<li>「カスタマイズ」の右にある▼をクリックし、<b>「HTMLを編集」</b>を選択</li>
<li>エディタ内をクリックし、<code>Ctrl + F</code>（MacはCmd + F）で <code>&lt;/body&gt;</code> を検索</li>
<li><code>&lt;/body&gt;</code> タグの<b>直前</b>に、以下のコードをコピーして貼り付けます</li>
</ol>

<p>以下のコードをコピーして、Blogger管理画面の「テーマ」→「HTML編集」で、<code>&lt;/body&gt;</code> タグの直前に貼り付けてください。</p>

<pre><code class="language-html">
&lt;!-- [START] 自動ブログカード化スクリプト --&gt;
&lt;script&gt;
//&lt;![CDATA[
document.addEventListener("DOMContentLoaded", function() {
  var postBodies = document.querySelectorAll(".post-body");
  postBodies.forEach(function(postBody) {
    var links = postBody.getElementsByTagName("a");
    for (var i = links.length - 1; i &gt;= 0; i--) {
      var link = links[i];
      if (link.href === link.textContent.trim() &amp;&amp; !link.querySelector('img')) {
        var iframe = document.createElement("iframe");
        iframe.setAttribute("src", "https://hatenablog-parts.com/embed?url=" + encodeURIComponent(link.href));
        iframe.setAttribute("style", "width:100%; height:190px; max-width:100%; margin: 10px 0; border:none; display:block;");
        iframe.setAttribute("scrolling", "no");
        iframe.setAttribute("frameborder", "0");
        iframe.setAttribute("loading", "lazy");
        var parent = link.parentNode;
        if (parent.textContent.trim() === link.href) {
            parent.insertBefore(iframe, link);
            link.style.display = "none";
        }
      }
    }
  });
});
//]]&gt;
&lt;/script&gt;
&lt;!-- [END] 自動ブログカード化スクリプト --&gt;
</code></pre>
<li>右上の保存ボタン（フロッピーアイコン）を押して保存します。</li>
<br />

    
## 使い方と注意点

<p>カスタマイズ後の記事の書き方には、簡単なルールがあります。</p>
<ul>
<li><b>URLを貼り付けてリンク化する</b><br />（BloggerのエディタでURLを貼り付け、リンクボタンを押して青文字の状態にします）</li>
<li><b>その行にはURL以外書かない</b><br />（「おすすめ→ https://...」のように文字が混ざっていると、テキストリンクのままになります）</li>
</ul>

<p>この仕組みは「はてなブログ」が提供している無料のブログカード機能を利用して表示させています。</p>
<p>とても簡単に見栄えが良くなるので、Bloggerユーザーの方はぜひ試してみてください。</p>


<hr />

    
## 【2026/02/19 追記】Microlink APIを使用した高速化＆デザイン刷新版


<p>上記のはてなブログカード版は手軽ですが、「デザインのカスタマイズができない」という欠点がありました。<br />
        そこで、より高速で、かつCSSで自由にデザインを変更できる<b>「Microlink API版」</b>にアップデートしました。</p>

<p>新しいコードは以下の通りです。基本的にはJavascriptを差し替え、CSSを追加するだけです。</p>

    
### 1. CSSの追加

<p><code>&lt;head&gt;</code> 内の <code>&lt;b:skin&gt;...&lt;/b:skin&gt;</code> 内、または
<code>&lt;style&gt;...&lt;/style&gt;</code> 内に以下を追加してください。</p>

<pre><code class="language-css">
/* ブログカードのデザイン */
.blog-card {
  display: flex !important;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08); /* 影を調整 */
  margin: 1.5em 0;
  text-decoration: none !important;
  color: #333 !important;
  overflow: hidden;
  height: 140px; /* 固定高さ */
  transition: all 0.3s ease;
}
.blog-card:hover {
  box-shadow: 0 4px 10px rgba(0,0,0,0.15); /* ホバー時の影 */
  transform: translateY(-2px);
  opacity: 1 !important;
}
.blog-card-thumbnail {
  width: 35%; /* 画像の幅 */
  min-width: 120px;
  max-width: 200px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  flex-shrink: 0;
  border-right: 1px solid #f0f0f0;
}
.blog-card-content {
  flex: 1;
  padding: 15px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.blog-card-meta {
  display: flex;
  align-items: center;
  font-size: 0.85em;
  color: #999;
  margin-bottom: 8px;
}
.blog-card-icon {
  width: 14px;
  height: 14px;
  margin-right: 6px;
  fill: #999;
}
.blog-card-title {
  font-size: 1.1em;
  font-weight: bold;
  line-height: 1.4;
  color: #333;
  margin: 0;
  max-height: 2.8em; /* 2行制限 */
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}
</code></pre>

    
### 2. JavaScriptの差し替え

<p>先ほどの <code>&lt;/body&gt;</code> 直前のスクリプトを、以下の新しいスクリプトに書き換えてください。</p>

<pre><code class="language-javascript">
&lt;script&gt;
//&lt;![CDATA[
document.addEventListener("DOMContentLoaded", function() {
  var postBodies = document.querySelectorAll(".post-body");
  postBodies.forEach(function(postBody) {
    var links = postBody.getElementsByTagName("a");
    // 配列に変換して処理
    for (var i = links.length - 1; i &gt;= 0; i--) {
      var link = links[i];
      var text = link.textContent.trim();
      var href = link.href;

      // URLのみのリンクかつ画像を含まない場合
      if ((href === text || href === text + "/") &amp;&amp; !link.querySelector('img')) {
        // 重複処理防止
        if (link.getAttribute('data-processed')) continue;
        link.setAttribute('data-processed', 'true');

        var parent = link.parentNode;
        // 親要素のテキストがリンクのテキストと一致（＝行全体がURLのみ）
        if (parent.textContent.trim() === text) {
           createBlogCard(link, parent);
        }
      }
    }
  });

  function createBlogCard(link, parent) {
      var url = link.href;
      
      // Microlink APIを使用してメタデータを取得 (JSON形式で高速)
      var apiUrl = 'https://api.microlink.io/?url=' + encodeURIComponent(url);
      
      fetch(apiUrl)
        .then(response =&gt; {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(json =&gt; {
            var data = json.data;
            if (!data || !data.title) throw new Error('No metadata found');

            var title = data.title;
            var image = data.image ? data.image.url : null;
            var dateStr = '';

            // 日付の取得
            if (data.date) {
                var date = new Date(data.date);
                if(!isNaN(date.getTime())) {
                    dateStr = date.getFullYear() + '年' + (date.getMonth()+1) + '月' + date.getDate() + '日';
                }
            }
            // 日付がなければドメインを表示
            if (!dateStr) {
                 dateStr = data.publisher || new URL(url).hostname;
            }

            // 画像がある場合のみカスタムカードを表示
            if (image) {
                var card = document.createElement('a');
                card.className = 'blog-card';
                card.href = url;
                card.target = '_blank';
                card.rel = 'noopener noreferrer';
                
                card.innerHTML = `
                  &lt;div class="blog-card-thumbnail" style="background-image: url('${image}')"&gt;&lt;/div&gt;
                  &lt;div class="blog-card-content"&gt;
                    &lt;div class="blog-card-meta"&gt;
                      &lt;svg class="blog-card-icon" viewBox="0 0 24 24"&gt;&lt;path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/&gt;&lt;/svg&gt;
                      &lt;span&gt;${dateStr}&lt;/span&gt;
                    &lt;/div&gt;
                    &lt;div class="blog-card-title"&gt;${title}&lt;/div&gt;
                  &lt;/div&gt;
                `;
                
                parent.insertBefore(card, link);
                link.style.display = 'none';
            } else {
                throw new Error('No image found');
            }
        })
        .catch(error =&gt; {
            // エラー時はHatenaブログカードにフォールバック
            var iframe = document.createElement("iframe");
            iframe.setAttribute("src", "https://hatenablog-parts.com/embed?url=" + encodeURIComponent(url));
            iframe.setAttribute("style", "width:100%; height:190px; max-width:100%; margin: 10px 0; border:none; display:block;");
            iframe.setAttribute("scrolling", "no");
            iframe.setAttribute("frameborder", "0");
            
            parent.insertBefore(iframe, link);
            link.style.display = "none";
        });
  }
});
//]]&gt;
&lt;/script&gt;
</code></pre>

<p>これで、よりリッチで高速なブログカードが表示されるようになります。万が一APIが動かない場合でも、自動的に旧来のはてなブログカードが表示される安全設計になっています。</p>
</article>




