import os
import requests
import json
import sys

MYFXBOOK_EMAIL = os.environ.get('MYFXBOOK_EMAIL')
MYFXBOOK_PASSWORD = os.environ.get('MYFXBOOK_PASSWORD')
ACCOUNT_ID = os.environ.get('MYFXBOOK_ACCOUNT_ID')

DAILY_GAIN_FILE = './static/data/myfxbook-data.json'
SUMMARY_FILE = './static/data/myfxbook-summary.json'
DATA_POINTS_FILE = './static/data/myfxbook-balance-points.json'
HISTORY_FILE = './static/data/myfxbook-history.json'
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

        os.makedirs('./static/data', exist_ok=True)

        # アカウントサマリー取得
        accounts_url = f"{API_BASE_URL}/get-my-accounts.json?session={session_id}"
        response = requests.get(accounts_url)
        response.raise_for_status()
        accounts_data = response.json()

        if accounts_data.get('error'):
            print(f"Accounts Fetch Error: {accounts_data.get('message')}")
            sys.exit(1)

        # 対象アカウントを抽出
        account = next(
            (a for a in accounts_data.get('accounts', []) if str(a.get('id')) == str(ACCOUNT_ID)),
            None
        )
        if not account:
            print(f"Error: アカウントID {ACCOUNT_ID} が見つかりません")
            sys.exit(1)

        summary = {
            "name":    account.get('name', ''),
            "balance": account.get('balance', 0),
            "currency": account.get('currency', 'USD'),
            "growth":  account.get('gain', 0),
            "drawdown": account.get('drawdown', 0),
            "monthly": account.get('monthly', 0),
        }
        with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=4)
        print(f"サマリー保存完了: {SUMMARY_FILE}")

        # Daily Gainデータ取得
        from datetime import datetime, timedelta
        end_date   = datetime.now().strftime('%m/%d/%Y')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%m/%d/%Y')
        data_url = (
            f"{API_BASE_URL}/get-daily-gain.json"
            f"?session={session_id}&id={ACCOUNT_ID}"
            f"&start={start_date}&end={end_date}"
        )
        response = requests.get(data_url)
        response.raise_for_status()
        daily_gain_data = response.json()

        if daily_gain_data.get('error'):
            print(f"Data Fetch Error: {daily_gain_data.get('message')}")
            sys.exit(1)

        with open(DAILY_GAIN_FILE, 'w', encoding='utf-8') as f:
            json.dump(daily_gain_data['dailyData'], f, ensure_ascii=False, indent=4)
        print(f"日次データ保存完了: {DAILY_GAIN_FILE}")

        # 残高推移データ取得（get-data-points）
        points_url = (
            f"{API_BASE_URL}/get-data-points.json"
            f"?session={session_id}&id={ACCOUNT_ID}"
            f"&start={start_date}&end={end_date}"
        )
        response = requests.get(points_url)
        response.raise_for_status()
        points_data = response.json()

        if points_data.get('error'):
            print(f"Data Points Error: {points_data.get('message')}")
        else:
            # [[datetime, balance, equity], ...] → [{date, balance, equity}, ...]
            formatted = [
                {"date": p[0], "balance": p[1], "equity": p[2]}
                for p in points_data.get('dataPoints', [])
            ]
            with open(DATA_POINTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(formatted, f, ensure_ascii=False, indent=4)
            print(f"残高推移データ保存完了: {DATA_POINTS_FILE}")

        # 取引履歴取得
        history_url = f"{API_BASE_URL}/get-history.json?session={session_id}&id={ACCOUNT_ID}"
        response = requests.get(history_url)
        response.raise_for_status()
        history_data = response.json()

        if history_data.get('error'):
            print(f"History Error: {history_data.get('message')}")
        else:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history_data.get('history', []), f, ensure_ascii=False, indent=4)
            print(f"取引履歴保存完了: {HISTORY_FILE}")

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
