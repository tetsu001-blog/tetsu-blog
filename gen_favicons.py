import os
from PIL import Image

static_dir = r'c:\Users\subli\プログラミング\blog\tetsu-blog-reborn\static'
source_image_path = os.path.join(static_dir, 'favicon.png')

if not os.path.exists(source_image_path):
    print(f'Error: {source_image_path} not found.')
    exit(1)

img = Image.open(source_image_path).convert('RGBA')

img.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(static_dir, 'apple-touch-icon.png'))
img.resize((32, 32), Image.Resampling.LANCZOS).save(os.path.join(static_dir, 'favicon-32x32.png'))
img.resize((16, 16), Image.Resampling.LANCZOS).save(os.path.join(static_dir, 'favicon-16x16.png'))
img.save(os.path.join(static_dir, 'favicon.ico'), format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

print('Successfully generated all favicons!')
