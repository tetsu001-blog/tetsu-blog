#!/usr/bin/env python3
"""
Obsidianが生成する画像パスをHugo用に自動変換するスクリプト。
git push の前に実行してください。

変換例:
  ![alt](static/images/xxx.png)  →  ![alt](/images/xxx.png)
  ![alt](../../static/images/xxx.png)  →  ![alt](/images/xxx.png)
"""

import re
import glob

def fix_image_paths():
    posts = glob.glob("content/posts/*.md")
    fixed_count = 0

    for filepath in posts:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Obsidianが生成する様々なパス形式をHugo用に変換
        new_content = re.sub(
            r'!\[([^\]]*)\]\((?:\.\.\/)*(?:static\/)?images\/([^)]+)\)',
            r'![\1](/images/\2)',
            content
        )

        # スペースを含むファイル名をハイフンに置換
        def replace_spaces(match):
            alt = match.group(1)
            path = match.group(2).replace(" ", "-")
            return f"![{alt}](/images/{path})"

        new_content = re.sub(
            r'!\[([^\]]*)\]\(/images/([^)]*\s[^)]*)\)',
            replace_spaces,
            new_content
        )

        if content != new_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            fixed_count += 1
            print(f"✅ 修正: {filepath}")

    if fixed_count == 0:
        print("✨ 修正が必要なファイルはありませんでした")
    else:
        print(f"\n📝 {fixed_count}件のファイルを修正しました")

if __name__ == "__main__":
    fix_image_paths()
