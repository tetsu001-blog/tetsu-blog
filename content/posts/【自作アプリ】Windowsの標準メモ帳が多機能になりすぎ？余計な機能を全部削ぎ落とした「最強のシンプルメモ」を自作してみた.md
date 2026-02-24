---
title: "【自作アプリ】Windowsの標準メモ帳が多機能になりすぎ？余計な機能を全部削ぎ落とした「最強のシンプルメモ」を自作してみた"
slug: "2026-02-13"
date: 2026-02-13T10:25:00Z
lastmod: 2026-02-19T05:38:42.025Z
draft: false
tags: ["デジタル", "雑記"]
categories: []
image: "/images/img_ca3dd4cb02e5.jpg"
---


<div class="separator" style="clear: both; text-align: center;">
<a href="/images/img_65d1dce18bc3.jpg" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="1024" data-original-width="1024" height="320" src="/images/img_ca3dd4cb02e5.jpg" width="320" /></a>
</div>
<br />こんにちは、てつです！


<p>
  突然ですが、皆さん。最近の<strong>Windows標準の「メモ帳」</strong>についてどう思いますか？
</p>

<p>
  タブ機能がついたり、Copilot（AI）が搭載されたり……。<br />
  進化しているのは分かるんです。分かるんですが、正直なところ<strong>「ちょっとお腹いっぱい」</strong>って感じることありませんか？
</p>

<p>
  「ただテキストを打ちたいだけなのに、起動が重い」<br />
  「右クリックメニューにAIが出てくるのが煩わしい」
</p>

<p>
  そんなふうにモヤモヤしていたので、今回は<strong>「私にとって本当に必要な機能だけのメモアプリ」</strong>を自作してみました！
</p>

<p>
  コード生成には話題のエディタ<strong>「Antigravity」</strong>を使用。AIの力を使って「AI機能を排除したアプリ」を作るという、なんだか皮肉で面白い試みです（笑）。
</p>



## 開発のきっかけ：Windowsメモ帳への「逆張り」


<p>
  今回のコンセプトは単純明快。<br />
<strong>「Windows標準のメモ帳から、無駄を削ぎ落とす」</strong>こと。
</p>

<p>
  高機能なエディタは世の中にたくさんありますが、私が欲しいのは「起動した瞬間に書ける」あの軽快さ。でも、余計なサジェストはいらない。
</p>

<p>
  そこで、Antigravity（AIコードエディタ）にこんなプロンプト（指示）を投げてみました。
</p>

<div style="background-color: #f9f9f9; border-radius: 8px; border: 1px solid rgb(204, 204, 204); box-shadow: rgba(0, 0, 0, 0.05) 0px 2px 5px; color: #333333; margin-bottom: 25px; padding: 20px;">
    
### 【プロンプトの要約】

<ul style="margin-bottom: 0px; padding-left: 20px;">
<li style="margin-bottom: 8px;"><strong>ベース：</strong>Windows標準のメモ帳ライクなもの</li>
<li style="margin-bottom: 8px;"><strong>言語：</strong>C# / WPF または WinForms</li>
<li style="margin-bottom: 8px;"><strong>基本機能：</strong>入力、編集、保存、読み込み、MSゴシック（等幅）デフォルト</li>
<li><strong>絶対にやらないこと（排除）：</strong>
<ul style="margin-top: 5px;">
<li style="margin-bottom: 5px;">Copilot/AI機能の完全排除（メニューにも出さない）</li>
<li>タブ機能の排除（クラシックな単一ウィンドウ）</li>
</ul>
</li>
</ul>
</div>

<p>
  ポイントは「機能の追加」ではなく<strong>「機能の排除」</strong>を明確に指示したこと。<br />
  これによって、昔ながらのサクサク動くメモ帳の骨格ができあがりました。
</p>



## シンプルすぎたので「私好みのスパイス」を追加


<p>
  ベースができたら、少しだけ便利機能が欲しくなるのが人情です。<br />
  でも、複雑にはしたくない。そこで追加したのは以下の3点。
</p>

<ul>
<li>テキスト配置（左揃え・中央揃え等）</li>
<li>箇条書きリスト化</li>
<li>ナンバリング</li>
</ul>

<p>
  そして、今回の開発で一番こだわった<strong>「独自機能」</strong>がこれです。
</p>


### 🖱️ ドラッグ＆ドロップで即保存！機能


<p>
  画面上に、あえてレトロな<strong>「フロッピーディスクのアイコン」</strong>を設置しました。<br />
  普通の保存ボタンではありません。
</p>

<p>
<strong>【機能のルール】</strong><br />
  このアイコンをマウスで掴んで、デスクトップにポイッとドラッグ＆ドロップすると……</p><p>
<strong>「現在入力されているテキストが、即座に.txtファイルとして保存される」</strong>
</p>

<p>
  ファイル名は<strong>「入力されたテキストの先頭10文字」</strong>が自動で採用されます。
</p>

<video controls style="width: 100%; max-width: 100%; height: auto; border-radius: 8px; display: block; margin: 2em auto; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
  <source src="/images/memo.mp4" type="video/mp4">
  お使いのブラウザは動画タグをサポートしていません。
</video>

<p>
  「名前をつけて保存」ダイアログを出して、場所を選んで、ファイル名を入力して……という手間がゼロ。直感的に「このメモ、デスクトップに置いておこう」ができるんです。
</p>


## 開発の裏話：アイコン設定でのつまづき


<p>
  順調に進んでいた開発ですが、最後の仕上げである「アプリアイコンの設定」で少しハマりました。
</p>

<p>
  アイコン画像を書き換えようとしたところ、エラーが発生。<br />
  どうやら、システムフォルダにアクセスする関係か、一時的に強い権限が必要だったようです。
</p>

<p>
<strong>解決策：</strong><br />
  ターミナルを「管理者として実行」し、そこからビルドコマンド（<code>npm run build</code>
  等）を走らせることで無事に突破！</p>


## まとめ：私だけの道具を作る楽しさ


<p>
  こうして完成した「私のメモアプリ」。<br />
  見た目は地味ですが、愛着は抜群です。
</p>

<ul>
<li>AIに邪魔されない</li>
<li>タブに埋もれない</li>
<li>直感的にファイルを保存できる</li>
</ul>

<p>
  既存のアプリに不満があるなら、私で作ってしまうのも一つの手ですね。特に「機能を減らす」というアプローチは、生産性を上げるに意外と効果的かもしれません。
</p>

<p>
  皆さんも「ここがこうだったらいいのに！」というツール、ありませんか？<br />
  もしあったら、ぜひコメントで教えてくださいね！
</p>




