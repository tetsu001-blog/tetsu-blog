import os
import glob
import re
from collections import defaultdict

posts_dir = r'c:\Users\subli\プログラミング\blog\tetsu-blog-reborn\content\posts'
files = glob.glob(os.path.join(posts_dir, '*.md'))

slug_to_files = defaultdict(list)

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'^slug:\s*\"?(.*?)\"?$', content, flags=re.MULTILINE)
    if m:
        slug = m.group(1).strip()
        slug_to_files[slug].append(file)

for slug, flist in slug_to_files.items():
    if len(flist) > 1:
        flist.sort(key=os.path.getmtime) # Sort by modification time
        for idx, file in enumerate(flist):
            new_slug = f'{slug}-{idx+1}'
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = re.sub(r'^slug:\s*\"?' + re.escape(slug) + r'\"?$', f'slug: "{new_slug}"', content, flags=re.MULTILINE)
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {os.path.basename(file)} to slug: {new_slug}')
