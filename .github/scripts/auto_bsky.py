import os
import sys
import xml.etree.ElementTree as ET
import re
from urllib.request import urlopen, Request
from datetime import datetime, timezone, timedelta

try:
    # OGPのブログカードを作成するための models を追加インポート
    from atproto import Client, client_utils, models
except ImportError:
    print("Error: 'atproto' library is not installed. Run 'pip install atproto'.")
    sys.exit(1)

try:
    from PIL import Image
    import io
except ImportError:
    print("Error: 'Pillow' library is not installed. Run 'pip install Pillow'.")
    sys.exit(1)

RSS_URL = 'https://tetsu-blog.pages.dev/index.xml'

def check_new_posts():
    """RSSフィードから過去24時間以内に公開された最新の投稿を取得する"""
    print(f"Fetching RSS feed from {RSS_URL}...")
    try:
        req = Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        response = urlopen(req)
        xml_data = response.read()
    except Exception as e:
        print(f"Failed to fetch RSS feed: {e}")
        return None

    root = ET.fromstring(xml_data)
    ns = {}

    items = root.findall('.//item', ns)
    if not items:
        print("No items found in RSS feed.")
        return None

    latest_item = items[0]
    title = latest_item.find('title', ns).text
    link = latest_item.find('link', ns).text
    pub_date_str = latest_item.find('pubDate', ns).text

    print(f"Latest post found: {title}")
    
    try:
        pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        return None

    now = datetime.now(timezone.utc)
    if (now - pub_date) > timedelta(hours=24):
        print("Latest post is older than 24 hours. Skipping auto-post.")
        return None

    return {"title": title, "link": link}

def get_ogp_info(url):
    """ブログのHTMLからOGP情報（タイトル、説明、サムネ画像）を抽出する"""
    print(f"Fetching OGP info for {url}...")
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        # HTMLを文字列として読み込む
        html = urlopen(req).read().decode('utf-8')
        
        # 正規表現でメタタグを検索
        title_m = re.search(r'<meta property="og:title" content="(.*?)"\s*/?>', html)
        desc_m = re.search(r'<meta property="og:description" content="(.*?)"\s*/?>', html)
        img_m = re.search(r'<meta property="og:image" content="(.*?)"\s*/?>', html)
        
        return {
            'title': title_m.group(1) if title_m else '',
            'description': desc_m.group(1) if desc_m else '',
            'image_url': img_m.group(1) if img_m else ''
        }
    except Exception as e:
        print(f"Failed to fetch OGP info: {e}")
        return {}

def post_to_bluesky(post_info):
    """取得した記事情報をBlueskyに「ブログカード付き」で投稿する"""
    handle = os.environ.get('BLUESKY_HANDLE')
    password = os.environ.get('BLUESKY_PASSWORD')

    if not handle or not password:
        sys.exit(1)

    print(f"Logging in to Bluesky as {handle}...")
    client = Client()
    try:
        client.login(handle, password)
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

    # 1. ブログ記事からOGP情報と画像を拾ってくる
    ogp = get_ogp_info(post_info['link'])
    thumb_blob = None
    
    # URLに画像が指定されていれば、Blueskyのサーバーに画像をアップする
    if ogp.get('image_url'):
        try:
            print(f"Downloading OGP image: {ogp['image_url']}")
            req = Request(ogp['image_url'], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            img_data = urlopen(req).read()
            
            # 画像データが1MB (Blueskyの制限) に近い場合、圧縮・リサイズする
            # Bluesky API limit is 1,000,000 bytes. We use 950,000 as a safe threshold.
            MAX_IMAGE_SIZE = 950000 
            
            if len(img_data) > MAX_IMAGE_SIZE:
                print(f"Image size ({len(img_data)} bytes) exceeds limits. Compressing...")
                try:
                    img = Image.open(io.BytesIO(img_data))
                    
                    # RGBモードでない場合（透過PNGファイル等）は変換
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # 初期品質設定
                    quality = 85
                    output_io = io.BytesIO()
                    
                    # リサイズループ
                    while len(img_data) > MAX_IMAGE_SIZE and quality > 10:
                        output_io.seek(0)
                        output_io.truncate()
                        img.save(output_io, format="JPEG", quality=quality)
                        img_data = output_io.getvalue()
                        print(f"Compressed to {len(img_data)} bytes with quality {quality}")
                        
                        if len(img_data) > MAX_IMAGE_SIZE:
                            # それでも大きい場合は半分のサイズに縮小
                            new_width = int(img.width * 0.8)
                            new_height = int(img.height * 0.8)
                            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                            quality -= 10
                            
                except Exception as compression_error:
                     print(f"Failed to compress image: {compression_error}")
                     # 圧縮に失敗した場合はそのままアップロードを試みるか、エラーにするか判断
                     # 今回はフォールバックとして圧縮前のデータを送信し、API側でのエラーに委ねる
            
            # Blueskyに画像データをアップロードして、ID (blob) を受け取る
            upload = client.upload_blob(img_data)
            thumb_blob = upload.blob
        except Exception as e:
            print(f"Failed to upload image blob: {e}")

    # 2. ブログカード（リンクプレビュー）の枠組みを作る
    embed_external = models.AppBskyEmbedExternal.Main(
        external=models.AppBskyEmbedExternal.External(
            title=ogp.get('title') or post_info['title'],
            description=ogp.get('description') or '記事を読む',
            uri=post_info['link'],
            thumb=thumb_blob
        )
    )

    # 3. 本文のテキストを作る
    tb = client_utils.TextBuilder()
    tb.text(f"新しい記事を公開しました！\n【{post_info['title']}】\n\n")
    tb.tag("#ブログ", "ブログ")
    tb.text(" ")
    tb.tag("#自動更新", "自動更新")
    # ※ブログカードを付ける場合、テキスト本文にURLリンク（tb.link）を直接入れなくてもカードがタップ可能になります。
    
    print("Posting to Bluesky with Link Card...")
    try:
        # 本文とブログカードを合体させて投稿！
        post = client.send_post(tb, embed=embed_external)
        print(f"Successfully posted! Post URI: {post.uri}")
    except Exception as e:
        print(f"Failed to post: {e}")
        sys.exit(1)

if __name__ == "__main__":
    post_info = check_new_posts()
    if post_info:
        post_to_bluesky(post_info)
    else:
        print("No new post to post to Bluesky today.")
