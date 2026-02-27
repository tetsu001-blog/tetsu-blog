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


def compress_images():
    """static/images/ 内のファイルサイズが950KBを超える画像を圧縮・リサイズする"""
    try:
        from PIL import Image
    except ImportError:
        print("[WARNING] Pillow is not installed. Skipping image compression.")
        return 0

    compressed_count = 0
    max_size = 950 * 1024  # 950 KB

    for filepath in glob.glob(os.path.join(STATIC_IMAGES, "*")):
        if not os.path.isfile(filepath):
            continue
            
        file_size = os.path.getsize(filepath)
        if file_size > max_size:
            print("[COMPRESS] {} ({:.1f} KB) is over 950KB. Compressing...".format(os.path.basename(filepath), file_size / 1024))
            try:
                img = Image.open(filepath)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                    
                quality = 85
                output_path = filepath + ".tmp.jpg"
                
                while True:
                    img.save(output_path, format="JPEG", quality=quality)
                    new_size = os.path.getsize(output_path)
                    
                    if new_size <= max_size or quality <= 10:
                        break
                        
                    new_width = int(img.width * 0.8)
                    new_height = int(img.height * 0.8)
                    try:
                        resample_filter = Image.Resampling.LANCZOS
                    except AttributeError:
                        resample_filter = Image.LANCZOS
                    img = img.resize((new_width, new_height), resample_filter)
                    quality -= 10
                
                orig_name = os.path.basename(filepath)
                new_name = os.path.splitext(orig_name)[0] + ".jpg"
                new_filepath = os.path.join(STATIC_IMAGES, new_name)
                
                if orig_name.lower().endswith((".jpg", ".jpeg")):
                    shutil.move(output_path, filepath)
                else:
                    shutil.move(output_path, new_filepath)
                    os.remove(filepath)
                    replace_image_in_markdown(orig_name, new_name)
                
                compressed_count += 1
                print("[COMPRESS] Successfully compressed to {:.1f} KB".format(new_size / 1024))

            except Exception as e:
                print("[ERROR] Failed to compress {}: {}".format(filepath, e))
                if os.path.exists(filepath + ".tmp.jpg"):
                    os.remove(filepath + ".tmp.jpg")
                    
    return compressed_count


def replace_image_in_markdown(old_name, new_name):
    posts = glob.glob("content/posts/*.md")
    for filepath in posts:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if old_name in content:
            new_content = content.replace(old_name, new_name)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("[RENAME] Updated {} -> {} in {}".format(old_name, new_name, os.path.basename(filepath)))


if __name__ == "__main__":
    print("--- fix_images start ---\n")

    moved = move_images()
    compressed = compress_images()
    fixed = fix_paths()

    print("\n--- result ---")
    if moved > 0:
        print("{} images moved to static/images/".format(moved))
    if compressed > 0:
        print("{} images compressed and resized".format(compressed))
    if fixed > 0:
        print("{} posts fixed".format(fixed))
    if moved == 0 and fixed == 0 and compressed == 0:
        print("Nothing to fix!")
    print("Done! Now run: git add . && git commit && git push")
