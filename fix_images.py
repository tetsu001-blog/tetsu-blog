#!/usr/bin/env python3
"""
Obsidianが保存した画像をHugo用に自動変換するスクリプト。
git push の前に実行してください。

やること:
1. content/images/ にある画像を static/images/ に移動
2. 記事内の画像パスをHugo用に変換
   例: ![alt](images/xxx.png) → ![alt](/images/xxx.png)
3. スペースを含むファイル名をハイフンに置換
"""

import re
import glob
import shutil
import os

CONTENT_IMAGES = os.path.join("content", "images")
STATIC_IMAGES = os.path.join("static", "images")


def move_images():
    """content/images/ の画像を static/images/ に移動"""
    if not os.path.exists(CONTENT_IMAGES):
        return 0

    moved = 0
    for filepath in glob.glob(os.path.join(CONTENT_IMAGES, "*")):
        filename = os.path.basename(filepath)
        # スペースをハイフンに置換
        safe_name = filename.replace(" ", "-")
        dest = os.path.join(STATIC_IMAGES, safe_name)

        if not os.path.exists(dest):
            shutil.move(filepath, dest)
            print(f"📁 移動: {filename} → static/images/{safe_name}")
            moved += 1
        else:
            os.remove(filepath)
            print(f"⏭️ 既存: {safe_name} (重複を削除)")

    # content/images/ が空なら削除
    try:
        os.rmdir(CONTENT_IMAGES)
    except OSError:
        pass

    # content/static/images/ も処理（前回のゴミ）
    content_static = os.path.join("content", "static", "images")
    if os.path.exists(content_static):
        for filepath in glob.glob(os.path.join(content_static, "*")):
            filename = os.path.basename(filepath)
            safe_name = filename.replace(" ", "-")
            dest = os.path.join(STATIC_IMAGES, safe_name)
            if not os.path.exists(dest):
                shutil.move(filepath, dest)
                moved += 1
            else:
                os.remove(filepath)
        try:
            os.rmdir(content_static)
            os.rmdir(os.path.join("content", "static"))
        except OSError:
            pass

    return moved


def fix_paths():
    """記事内の画像パスをHugo用に変換"""
    posts = glob.glob("content/posts/*.md")
    fixed_count = 0

    for filepath in posts:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Obsidianが生成する様々なパス形式をHugo用に変換
        # images/xxx.png → /images/xxx.png
        # static/images/xxx.png → /images/xxx.png
        # ../static/images/xxx.png → /images/xxx.png
        new_content = re.sub(
            r'!\[([^\]]*)\]\((?:\.\.\/)*(?:static\/)?images\/([^)]+)\)',
            r'![\1](/images/\2)',
            content
        )

        # スペースを含むファイル名をハイフンに置換
        def replace_spaces(match):
            alt = match.group(1)
            path = match.group(2).replace("%20", "-").replace(" ", "-")
            return f"![{alt}](/images/{path})"

        new_content = re.sub(
            r'!\[([^\]]*)\]\(/images/([^)]*(?:%20|\s)[^)]*)\)',
            replace_spaces,
            new_content
        )

        if content != new_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            fixed_count += 1
            print(f"✅ パス修正: {os.path.basename(filepath)}")

    return fixed_count


if __name__ == "__main__":
    print("🔧 画像の整理を開始...\n")

    moved = move_images()
    fixed = fix_paths()

    print(f"\n{'='*40}")
    if moved > 0:
        print(f"📁 {moved}個の画像を static/images/ に移動")
    if fixed > 0:
        print(f"✅ {fixed}個の記事のパスを修正")
    if moved == 0 and fixed == 0:
        print("✨ 修正が必要なファイルはありませんでした")
    print("完了！git add → commit → push してください")
