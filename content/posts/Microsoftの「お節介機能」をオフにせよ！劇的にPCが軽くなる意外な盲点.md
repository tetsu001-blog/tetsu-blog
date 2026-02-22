---
title: "Microsoftの「お節介機能」をオフにせよ！劇的にPCが軽くなる意外な盲点"
slug: "2026-01-05"
date: 2026-01-05T08:37:00Z
lastmod: 2026-02-03T00:43:38.346Z
draft: false
tags: []
categories: []
image: "/images/img_8d6e7a2413e5.jpg"
---


<div class="separator" style="clear: both; text-align: center;">
<a href="/images/img_b0f860a87bad.jpg" style="margin-left: 1em; margin-right: 1em;"><img data-original-height="572" data-original-width="1024" height="358" src="/images/img_8d6e7a2413e5.jpg" width="640" /></a>
</div>
<br />

<p>
  「最近、何もしていないのにパソコンのファンがうるさい」「動作がもっさりして重い」と感じていませんか？
</p>
<p>
  パソコンの価格が高騰している今、数年前なら10万円で買えたスペックが、今では15〜20万円ほどすることもあり、簡単に買い替えるのは難しいですよね。そこで今回は、今あるパソコンを少しでも長く、快適に使うために、Windowsの動作を重くしている「原因」と、誰でもできる「軽量化設定」をご紹介します。
</p>


## まずは現状を確認：メモリ使用率をチェック

<p>
  設定を変更する前に、あなたのパソコンがどれくらいピンチなのか確認してみましょう。
</p>
<ol>
<li>タスクバーの上で右クリックし、「タスクマネージャー」を起動します。</li>
<li>「パフォーマンス」をクリックし、「メモリ」を選びます。</li>
</ol>
<p>
  もし、重い作業をしていないのに使用率が<strong>60%を超えていたら危険な状態</strong>、<strong>80%を超えていたらパソコンが悲鳴を上げている状態</strong>です。
</p>
<p>
  以下で紹介する設定を行うことで、メモリやCPUの無駄遣いを減らし、パソコンを爆速化できる可能性があります。
</p>
<hr />

## 原因1：2026年最新の「強制自動化」プログラム (KB5072033)

<p>
  2026年の年明け以降、急激に重くなった場合は、Windows
  Update（KB5072033）が原因の可能性があります。
</p>

### 犯人は「AppXSVC」

<p>
  これまで必要な時だけ動いていた「AppXSVC（AppX Deployment
  Service）」というプログラムが、OS起動と同時に強制的にフル稼働する仕様に変更されました。これにより、通常時は20MB程度のメモリ消費だったものが、暴走すると800MB〜数GBも消費し、CPUやディスク使用率を圧迫することがあります。
</p>
<p>
<b>これはMicrosoft
    Storeアプリの管理やAI連携のための変更ですが、ユーザーにとってはPCを重くする原因になりかねません。</b>
</p><p><b><br /></b></p>

### 対処法：レジストリで無効化する

<p>
  この機能は通常の「サービス」画面からは無効化できないようロックされています。そのため、レジストリエディターを使用します。
</p>

<div class="separator" style="clear: both; text-align: center;">
<a href="/images/img_57b490144571.jpg" style="margin-left: 1em; margin-right: 1em;"><img data-original-height="768" data-original-width="1408" height="219" src="/images/img_4c642e350b94.jpg" width="400" /></a>
</div>


<p>
<span><span style="font-size: large;">&nbsp;<span style="color: #ffe599;">
</span></span><b><span style="color: #ffe599; font-size: x-large;">※レジストリ操作はリスクを伴うため、システムの復元ポイントを作成するなど、自己責任で行ってください。</span></b></span>
</p>
<p>
<span style="font-size: medium;"><b><br /></b></span>
</p>

#### <ul style="text-align: left;"><li>検索ボックスに「regedit」と入力し、<strong>レジストリエディター</strong>を起動します。</li></ul>
<ol style="text-align: left;">
</ol>
<div>
<div class="separator" style="clear: both; text-align: center;">
<a href="/images/img_31eec729f8a5.jpg" style="margin-left: 1em; margin-right: 1em;"><img data-original-height="515" data-original-width="757" height="272" src="/images/img_b80686bcc06b.jpg" width="400" /></a>
</div>
<br />
</div>

#### <ul style="text-align: left;"><li>画面上部にあるアドレスバーにアドレスを入力します。[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AppXSVC]</li></ul>
<ol style="text-align: left;">
</ol>
<div>
<div class="separator" style="clear: both; text-align: center;">
<a href="/images/img_fc130e4ad1f2.jpg" style="margin-left: 1em; margin-right: 1em;"><img data-original-height="450" data-original-width="1426" height="126" src="/images/img_3cb100d39d54.jpg" width="400" /></a>
</div>
<br /><br />
</div>

#### <ul style="text-align: left;"><li>画面右側の「Start」という項目をダブルクリックします。</li></ul>
<ol style="text-align: left;">
</ol>

#### <ul style="text-align: left;"><li>数値を<b>「2（自動）」から「3（手動）」</b>に書き換えてOKを押し、PCを再起動します。</li></ul>
<ol style="text-align: left;">
</ol>
<div>
<div class="separator" style="clear: both; text-align: center;">
<a href="/images/img_32ce0fed11ad.jpg" style="margin-left: 1em; margin-right: 1em;"><img data-original-height="311" data-original-width="961" height="130" src="/images/img_29f2ebd7f1df.jpg" width="400" /></a>
</div>
<br /><br />
</div>
<div></div>

## 原因2：Windowsの「メモリ泥棒」機能（基本の軽量化）

<p>
  最新の更新以外にも、Windowsには以前からメモリを無駄食いする<b>「隠れ犯人」</b>が存在します。以下の2つを見直すだけで、軽くなることがあります。
</p>


### ① 配信の最適化

<p>
  これは、あなたのPC内のアップデートファイルを、インターネット上の「他の誰かのPC」に配るために使われる機能です。勝手に通信を行い、メモリを消費します。
</p>

#### <strong>【無効化の手順】</strong>

<ul>
<li>
<strong>Windows 11：</strong> 設定 &gt; Windows Update &gt; 詳細オプション
    &gt; 配信の最適化 &gt;
    「他のデバイスからのダウンロードを許可する」を<strong>オフ</strong>にする。
</li>
<li>
<strong>Windows 10：</strong> 設定 &gt; 更新とセキュリティ &gt; 配信の最適化
    &gt; 「他のPCからのダウンロードを許可する」を<strong>オフ</strong>にする。
</li>
</ul>
<p>
  これを行っても、Microsoftから直接ダウンロードする通常の状態に戻るだけなので問題ありません。
</p>


### ② SysMain (旧 SuperFetch)

<p>
  あなたが次によく使うアプリを予測して、あらかじめメモリに読み込んでおく機能です。メモリ容量が少ないPCやHDD搭載機では、この「先読み」作業自体が重荷になり、動作を遅くする本末転倒な状態になることがあります。
</p>


#### <strong>【無効化の手順】</strong>

<ol>
<li>検索ボックスに<b>「サービス」</b>と入力して起動。</li>
<li>一覧から<b>「SysMain」</b>を探してダブルクリック。</li>
<li>「スタートアップの種類」を<b>「無効」</b>に変更。</li>
<li>
    「サービスの状態」が実行中なら<b>「停止」</b>を押し、最後に<b>「適用」→「OK」</b>をクリック。
</li>
</ol>



## まとめ：設定を見直してPCを延命しよう

<p>
  今回紹介した<b>「配信の最適化」</b>や<b>「SysMain」</b>を停止するだけで、メモリ使用率が15%（約2GB）も下がったケースがあります。特にスペックが低めのパソコンほど効果を実感しやすいはずです。
</p>
<p>
  「重いから買い替えなきゃ…」と諦める前に、まずはこれらの設定を試して、愛用のPCのポテンシャルを取り戻してみてください！
</p>

<div class="separator" style="clear: both; text-align: center;">
<a href="/images/img_c283d79dc2b6.jpg" style="margin-left: 1em; margin-right: 1em;"><img data-original-height="768" data-original-width="1408" height="219" src="/images/img_582c004894fd.jpg" width="400" /></a>
</div>
<br /><br />



