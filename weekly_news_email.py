#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime

# メール設定
TO_ADDRESS = "pubsky@outlook.jp"
FROM_ADDRESS = "pubsky@outlook.jp"
SUBJECT = "【週次ニュースまとめ】2026/03/23〜2026/03/29"

# SMTP設定（環境変数優先、なければデフォルト値）
SMTP_HOST = "smtp-mail.outlook.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get("SMTP_USER", "pubsky@outlook.jp")
SMTP_PASS = os.environ.get("SMTP_PASS", "")

BODY = """今週の主要ニュースをお届けします。

🏛️ 政治・行政
・2026年度予算案が年度内成立できず、政府が11日間の暫定予算案（総額約8.6兆円）を閣議決定
・高市首相が訪米しトランプ大統領と初の日米首脳会談、中東情勢・通商・安全保障を協議

💴 経済・ビジネス
・春闘2026：連合の賃上げ率は加重平均5.26%、7年連続で5%台維持の公算
・日銀が政策金利を0.75%に据え置き、ドル円は159円台まで円安が進行。日経平均は52,000円台で推移

🌍 国際・外交
・日米首脳会談でトランプ大統領が真珠湾に言及、各国メディアで大きく報道
・海上自衛隊の護衛艦「ちょうかい」が米国でトマホーク搭載改修を完了、9月に帰国予定

📱 社会・生活
・漫画家・つげ義春さんが3月3日に88歳で死去（27日に発表）。『ねじ式』『無能の人』などの代表作で知られる
・東京・名古屋で桜が平年より早く開花。DV相談が98,000件と過去最多を更新

🤖 テクノロジー
・東京発AIスタートアップ「Sakana AI」が日本仕様LLM「Namazu（ナマズ）」α版と無料チャットサービスを公開
・OpenAIが動画生成AIサービス「Sora」の全面終了を発表。リリースからわずか半年での撤退

⚾ スポーツ
・大相撲春場所：霧島が3度目の優勝で大関返り咲きを達成（3月25日）
・第6回WBC開幕、侍ジャパンが連覇を目指して出場。世界フィギュア選手権も3月25日開幕

---
このメールはClaude Codeによって自動生成されました。
"""


def send_email(label=""):
    """Outlook SMTP経由でメール送信"""
    password = SMTP_PASS or os.environ.get("SMTP_PASS", "")
    if not password:
        print("[エラー] SMTP_PASS 環境変数が設定されていません")
        return False

    msg = MIMEText(BODY, 'plain', 'utf-8')
    msg['Subject'] = Header(SUBJECT, 'utf-8')
    msg['From'] = FROM_ADDRESS
    msg['To'] = TO_ADDRESS

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, password)
            server.sendmail(FROM_ADDRESS, [TO_ADDRESS], msg.as_string())
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[成功]{' ' + label if label else ''} {ts} → {TO_ADDRESS}")
        return True
    except Exception as e:
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[失敗]{' ' + label if label else ''} {ts} : {e}")
        return False


if __name__ == "__main__":
    import sys
    label = sys.argv[1] if len(sys.argv) > 1 else ""
    send_email(label)
