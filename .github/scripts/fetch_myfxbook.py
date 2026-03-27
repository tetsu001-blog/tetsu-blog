import os
import requests
import json
import sys

MYFXBOOK_EMAIL = os.environ.get('MYFXBOOK_EMAIL')
MYFXBOOK_PASSWORD = os.environ.get('MYFXBOOK_PASSWORD')
ACCOUNT_ID = os.environ.get('MYFXBOOK_ACCOUNT_ID')

OUTPUT_FILE = './static/data/myfxbook-data.json'
API_BASE_URL = 'https://www.myfxbook.com/api'

def fetch_myfxbook_data():
    if not all([MYFXBOOK_EMAIL, MYFXBOOK_PASSWORD, ACCOUNT_ID]):
        print("Error: MYFXBOOK_EMAIL, MYFXBOOK_PASSWORD, MYFXBOOK_ACCOUNT_ID が設定されていません")
        sys.exit(1)

    session_id = None
    try:
        # ログイン
        login_url = f"{API_BASE_URL}/login.json?email={MYFXBOOK_EMAIL}&password={MYFXBOOK_PASSWORD}"
        response = requests.get(login_url)
        response.raise_for_status()
        login_data = response.json()

        if login_data.get('error'):
            print(f"Login Error: {login_data.get('message')}")
            sys.exit(1)

        session_id = login_data['session']
        print("ログイン成功")

        # Daily Gainデータ取得
        data_url = f"{API_BASE_URL}/get-daily-gain.json?session={session_id}&id={ACCOUNT_ID}"
        response = requests.get(data_url)
        response.raise_for_status()
        daily_gain_data = response.json()

        if daily_gain_data.get('error'):
            print(f"Data Fetch Error: {daily_gain_data.get('message')}")
            sys.exit(1)

        # JSONファイルに保存
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(daily_gain_data['dailyData'], f, ensure_ascii=False, indent=4)
        print(f"データ保存完了: {OUTPUT_FILE}")

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: JSONのデコードに失敗しました")
        sys.exit(1)
    finally:
        if session_id:
            logout_url = f"{API_BASE_URL}/logout.json?session={session_id}"
            requests.get(logout_url)
            print("ログアウト完了")

if __name__ == "__main__":
    fetch_myfxbook_data()
