import os
import requests
import json
import sys
from datetime import datetime, timedelta

MYFXBOOK_EMAIL    = os.environ.get('MYFXBOOK_EMAIL')
MYFXBOOK_PASSWORD = os.environ.get('MYFXBOOK_PASSWORD')
ACCOUNT_ID        = os.environ.get('MYFXBOOK_ACCOUNT_ID')

SUMMARY_FILE    = './static/data/myfxbook-summary.json'
DAILY_GAIN_FILE = './static/data/myfxbook-data.json'
HISTORY_FILE    = './static/data/myfxbook-history.json'
API_BASE_URL    = 'https://www.myfxbook.com/api'

def api_get(url):
    """GETリクエストを送り、JSONを返す。失敗時はNoneを返す。"""
    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"  警告: {e}")
        return None

def fetch_myfxbook_data():
    if not all([MYFXBOOK_EMAIL, MYFXBOOK_PASSWORD, ACCOUNT_ID]):
        print("Error: MYFXBOOK_EMAIL, MYFXBOOK_PASSWORD, MYFXBOOK_ACCOUNT_ID が設定されていません")
        sys.exit(1)

    # --- ログイン（必須） ---
    login_data = api_get(f"{API_BASE_URL}/login.json?email={MYFXBOOK_EMAIL}&password={MYFXBOOK_PASSWORD}")
    if not login_data or login_data.get('error'):
        print(f"Login Error: {login_data.get('message') if login_data else '接続失敗'}")
        sys.exit(1)

    session_id = login_data['session']
    print("ログイン成功")
    os.makedirs('./static/data', exist_ok=True)

    try:
        # --- アカウントサマリー（必須） ---
        accounts_data = api_get(f"{API_BASE_URL}/get-my-accounts.json?session={session_id}")
        if not accounts_data or accounts_data.get('error'):
            print(f"Accounts Error: {accounts_data.get('message') if accounts_data else '取得失敗'}")
            sys.exit(1)

        account = next(
            (a for a in accounts_data.get('accounts', []) if str(a.get('id')) == str(ACCOUNT_ID)),
            None
        )
        if not account:
            print(f"Error: アカウントID {ACCOUNT_ID} が見つかりません")
            sys.exit(1)

        summary = {
            "name":        account.get('name', ''),
            "balance":     account.get('balance', 0),
            "currency":    account.get('currency', 'USD'),
            "growth":      account.get('gain', 0),
            "absGain":     account.get('absGain', 0),
            "daily":       account.get('daily', 0),
            "monthly":     account.get('monthly', 0),
            "drawdown":    account.get('drawdown', 0),
            "equity":      account.get('equity', 0),
            "equityPercent": account.get('equityPercent', 0),
            "highest":     account.get('highest', 0),
            "profit":      account.get('profit', 0),
            "interest":    account.get('interest', 0),
            "deposits":    account.get('deposits', 0),
            "withdrawals": account.get('withdrawals', 0),
        }
        with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=4)
        print(f"サマリー保存完了: {SUMMARY_FILE}")

        # --- Daily Gain（任意） ---
        end_date   = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        daily_data = api_get(
            f"{API_BASE_URL}/get-daily-gain.json"
            f"?session={session_id}&id={ACCOUNT_ID}"
            f"&start={start_date}&end={end_date}"
        )
        if daily_data and not daily_data.get('error'):
            with open(DAILY_GAIN_FILE, 'w', encoding='utf-8') as f:
                json.dump(daily_data.get('dailyGain', []), f, ensure_ascii=False, indent=4)
            print(f"日次データ保存完了: {DAILY_GAIN_FILE}")
        else:
            print(f"Daily Gain スキップ: {daily_data.get('message') if daily_data else '取得失敗'}")

        # --- 取引履歴（任意） ---
        history_data = api_get(
            f"{API_BASE_URL}/get-history.json?session={session_id}&id={ACCOUNT_ID}"
        )
        if history_data and not history_data.get('error'):
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history_data.get('history', []), f, ensure_ascii=False, indent=4)
            print(f"取引履歴保存完了: {HISTORY_FILE}")
        else:
            print(f"取引履歴 スキップ: {history_data.get('message') if history_data else '取得失敗'}")

    finally:
        api_get(f"{API_BASE_URL}/logout.json?session={session_id}")
        print("ログアウト完了")

if __name__ == "__main__":
    fetch_myfxbook_data()
