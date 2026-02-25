#!/usr/bin/env python3
"""
Obsidianが保存した画像をHugo用に自動変換するスクリプト。
git push の前に実行してください。

やること:
1. content/images/ にある画像を static/images/ に移動
2. 記事内の画像パスをHugo用に変換
   例: ![alt](images/xxx.png) -> ![alt](/images/xxx.png)
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
        safe_name = filename.replace(" ", "-")
        dest = os.path.join(STATIC_IMAGES, safe_name)

        if not os.path.exists(dest):
            shutil.move(filepath, dest)
            print("[MOVE] {} -> static/images/{}".format(filename, safe_name))
            moved += 1
        else:
            os.remove(filepath)
            print("[SKIP] {} (already exists)".format(safe_name))

    try:
        os.rmdir(CONTENT_IMAGES)
    except OSError:
        pass

    # content/static/images/ も処理
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

        new_content = re.sub(
            r'!\[([^\]]*)\]\((?:\.\.\/)*(?:static\/)?images\/([^)]+)\)',
            r'![\1](/images/\2)',
            content
        )

        def replace_spaces(match):
            alt = match.group(1)
            path = match.group(2).replace("%20", "-").replace(" ", "-")
            return "![{}](/images/{})".format(alt, path)

        new_content = re.sub(
            r'!\[([^\]]*)\]\(/images/([^)]*(?:%20|\s)[^)]*)\)',
            replace_spaces,
            new_content
        )

        if content != new_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            fixed_count += 1
            print("[FIX] {}".format(os.path.basename(filepath)))

        # ここから追加：サムネイル画像の自動設定
        with open(filepath, "r", encoding="utf-8") as f:
            updated_content = f.read()

        # サムネイル用の画像タグを検索
        thumb_match = re.search(r'<!-- thumbnail_start -->\s*!\[.*?\]\((.*?)\)\s*<!-- thumbnail_end -->', updated_content)
        
        if thumb_match:
            image_path = thumb_match.group(1)
            # imageプロパティを更新
            final_content = re.sub(
                r'^image:.*$',
                f'image: "{image_path}"',
                updated_content,
                flags=re.MULTILINE
            )
            
            if updated_content != final_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(final_content)
                print("[THUMBNAIL SET] {} -> {}".format(os.path.basename(filepath), image_path))
    return fixed_count


if __name__ == "__main__":
    print("--- fix_images start ---\n")

    moved = move_images()
    fixed = fix_paths()

    print("\n--- result ---")
    if moved > 0:
        print("{} images moved to static/images/".format(moved))
    if fixed > 0:
        print("{} posts fixed".format(fixed))
    if moved == 0 and fixed == 0:
        print("Nothing to fix!")
    print("Done! Now run: git add . && git commit && git push")
