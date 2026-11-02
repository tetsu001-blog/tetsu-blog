# ブログ運用・開発ルール

てつblog（`tetsu-blog.net`）は Hugo 製の静的サイト_generator。ローカル運営と公開運用の**両方で**下列ルールを適用すること。

---

## 1. 画像処理スクリプト（fix_images.py）の自動実行ルール

ユーザーから以下のような自然言語による指示やリクエストがあった場合、AIは自動的に `fix_images.py` を実行してください。

### 実行トリガー（発話例）

- 「画像パスを整えて」「画像パスを修正して」
- 「画像を修正して」「画像変換して」
- 「Obsidianの画像をHugo用に変換して」
- 「画像のリンクチェック・最適化をして」
- 「fix_imagesを実行して」

### 実行時の処理

**どのディレクトリから実行しても構いません**（スクリプトが自身の位置を基準にパスを解決するため）。

```bash
python tetsu-blog-reborn/fix_images.py   # blog/ 直下から
python fix_images.py                      # tetsu-blog-reborn/ 直下から
```

スクリプトが行う処理:

1. `content/images/`（Obsidianの貼り付け先）の画像を `static/images/` へ移動（ファイル名の空白をハイフンに置換）
2. 記事内の画像パスを Hugo 形式へ変換（`![](images/x.png)` → `![](/images/x.png)`）
3. `<!-- thumbnail_start -->`〜`<!-- thumbnail_end -->` の画像から front matter の `image:` を自動同期
4. `static/images/` 内の 950KB 超の画像を JPEG へ圧縮・リサイズし、記事内の参照を自動更新

### 実行後の報告

スクリプトの実行結果（移動・圧縮された画像、修正された記事ファイルなど）をユーザーに報告すること。

---

## 2. 記事作成ルール

### front matter（必須項目）

```yaml
---
title: "【見出し】記事タイトル"
description: "SNSカード用の概要（80〜120字程度）"
date: 2026-10-22T15:30:00
draft: true              # 下書き中は必ず true
tags:
  - デジタル
categories:
  - デジタル
image: "/images/xxx.png"
slug: article-slug
---
```

- `title` / `description` は**引用符で囲む**
- `draft: true` の記事は Hugo の通常ビルドにも RSS にも**出力されない**（Bluesky 自動投稿は RSS 連動のため、`draft: true` のままなら自動投稿も走らない）
- `slug` はASCIIの kebab-case
- `image` は `static/images/` に実在するファイルへのパス。先頭スラッシュ必須

### 下書きと投稿の区別

- ユーザーが「下書き」「draft にして」と指示された場合は `draft: true` のまま保存し、**投稿しない**
- 公開の明示指示があった場合のみ `draft: false` に変更する
- Git 操作（`git add` / `git commit` / `git push`）は、**ユーザーからの明示的な指示がない限り絶対に実行しない**

### 本文の書き方

- 日本語で書く
- 冒頭に「こんにちは、てつです！」で入り、**過去記事のトーン**に合わせる（`content/posts/` の直近記事を必ず読んでから書く）
- 重要箇所は `**太字**`、表は Markdown テーブル、箇条書きは `-`
- 文章中に**中国語の混入・機械翻訳臭・不要な英単語の混入がないこと**を必ず確認する
- 事実（数値・CVE ID・組織名・日時）は一次ソースで確認し、出典を記事末尾の「参考・出典」subsectionにまとめる

---

## 3. 画像に関する注意

- 画像は `content/images/` に貼り付け、`fix_images.py` で `static/images/` へ移動するのが既定フロー
- 一覧カード・OGP は `aspect-video` + `object-cover` で**中央帯だけ**が表示される。**正方形の画像は上下が切れる**ため、16:9（1024×572〜1200×630）で別途クロップ版を用意し `image:` に指定する
- 本文中の縦長画像は `max-width` を指定して拡大ブリングを避ける

---

## 4. ディレクトリ構成

```
blog/
├── .claude/                      # Claude Code のローカル権限設定
├── .agent/skills/                # MCode 用のスキル定義
├── tetsu-blog-reborn/            # ★実際のリポジトリ（Git管理対象）
│   ├── CLAUDE.md                 # 本ファイル
│   ├── GEMINI.md                 # Gemini CLI 向けルール
│   ├── fix_images.py             # 画像変換スクリプト
│   ├── hugo.toml
│   ├── content/posts/*.md        # 記事
│   ├── static/images/            # 配信画像
│   └── layouts/                  # テーマ
└── temp_prev.txt
```

- Hugo ビルド: `hugo` / プレビュー（draft込み）: `hugo server -D`
- `public/` は Git 管理外（`.gitignore` 済み）
