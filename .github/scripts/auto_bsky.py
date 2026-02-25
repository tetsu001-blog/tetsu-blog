import os
import sys
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from datetime import datetime, timezone, timedelta

# Bluesky API用のライブラリ (atproto) をインポート。GitHub Actions側で事前にpip install atprotoされる前提
try:
    from atproto import Client, client_utils
except ImportError:
    print("Error: 'atproto' library is not installed. Run 'pip install atproto'.")
    sys.exit(1)

# RSSフィードのURL（本番環境）
RSS_URL = 'https://tetsu-blog.pages.dev/index.xml'

def check_new_posts():
    """RSSフィードから過去24時間以内に公開された最新の投稿を取得する"""
    print(f"Fetching RSS feed from {RSS_URL}...")
    try:
        response = urlopen(RSS_URL)
        xml_data = response.read()
    except Exception as e:
        print(f"Failed to fetch RSS feed: {e}")
        return None

    root = ET.fromstring(xml_data)
    
    # RSSのnamespace (必要であれば追加)
    ns = {}

    items = root.findall('.//item', ns)
    if not items:
        print("No items found in RSS feed.")
        return None

    # 最新の1件を取得（一番上が最新と仮定）
    latest_item = items[0]
    title = latest_item.find('title', ns).text
    link = latest_item.find('link', ns).text
    pub_date_str = latest_item.find('pubDate', ns).text # 例: Tue, 24 Feb 2026 21:00:00 +0900

    print(f"Latest post found: {title}")
    print(f"Published at: {pub_date_str}")

    # 日付パース
    try:
        # RSSフォーマットの日付をパース
        pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        print(f"Failed to parse date: {pub_date_str}")
        return None

    # 今日（実行時から過去24時間以内）公開された記事かチェック
    now = datetime.now(timezone.utc)
    if (now - pub_date) > timedelta(hours=24):
        print("Latest post is older than 24 hours. Skipping auto-post.")
        return None

    return {"title": title, "link": link}

def post_to_bluesky(post_info):
    """取得した記事情報をBlueskyに投稿する"""
    handle = os.environ.get('BLUESKY_HANDLE')
    password = os.environ.get('BLUESKY_PASSWORD')

    if not handle or not password:
        print("Error: BLUESKY_HANDLE and BLUESKY_PASSWORD must be set in Environment Variables.")
        sys.exit(1)

    print(f"Logging in to Bluesky as {handle}...")
    client = Client()
    try:
        client.login(handle, password)
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

    # 投稿文の作成
    text_content = f"新しい記事を公開しました！\n【{post_info['title']}】\n\n#ブログ #自動更新"
    
    # atprotoのBuilderを使ってリンク付きの文章を作成する
    tb = client_utils.TextBuilder()
    tb.text(f"新しい記事を公開しました！\n【{post_info['title']}】\n\n")
    tb.tag("#ブログ", "ブログ")
    tb.text(" ")
    tb.tag("#自動更新", "自動更新")
    tb.text("\n")
    tb.link(post_info['link'], post_info['link'])

    print("Posting to Bluesky...")
    try:
        # OGPカードの自動作成など高度な設定も可能だが、
        # まずは一番シンプルなリンクテキスト付きのポストとして発信。
        # OGPを付けたい場合はURLをパースしてfacetを設定する処理が必要。
        # リンク（Tb）を設定すればBluesky公式アプリなどが勝手にカードを展開してくれることが多い。
        post = client.send_post(tb)
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
