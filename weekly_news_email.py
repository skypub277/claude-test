#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime

# メール設定
TO_ADDRESS = "pubsky@outlook.jp"
FROM_ADDRESS = "noreply@localhost"
SUBJECT = "【週次ニュースまとめ】2026/03/23〜2026/03/29"

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

def send_email_localhost():
    """ローカルSMTP (port 25) でメール送信を試みる"""
    msg = MIMEText(BODY, 'plain', 'utf-8')
    msg['Subject'] = Header(SUBJECT, 'utf-8')
    msg['From'] = FROM_ADDRESS
    msg['To'] = TO_ADDRESS

    try:
        with smtplib.SMTP('localhost', 25, timeout=10) as server:
            server.sendmail(FROM_ADDRESS, [TO_ADDRESS], msg.as_string())
        print(f"[成功] メールをlocalhostのSMTP経由で送信しました")
        print(f"送信先: {TO_ADDRESS}")
        print(f"件名: {SUBJECT}")
        print(f"送信日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
    except Exception as e:
        print(f"[失敗] localhost SMTP: {e}")
        return False

if __name__ == "__main__":
    print("=== 週次ニュースまとめメール送信 ===")
    print(f"送信先: {TO_ADDRESS}")
    print(f"件名: {SUBJECT}")
    print()
    print("--- メール本文プレビュー ---")
    print(BODY)
    print("---------------------------")
    print()

    # 方法B: ローカルSMTPを試みる
    success = send_email_localhost()

    if not success:
        print()
        print("[情報] ローカルSMTPサーバーが利用できません。")
        print("外部SMTPサーバー（Gmail等）を使用する場合は、以下の認証情報が必要です：")
        print("  - SMTPサーバー: smtp.gmail.com:587")
        print("  - ユーザー名: Gmailアドレス")
        print("  - パスワード: アプリパスワード")
        print()
        print("または以下のコマンドでメール本文をファイルに保存しました：")
        with open('/home/user/claude-test/email_body.txt', 'w', encoding='utf-8') as f:
            f.write(f"To: {TO_ADDRESS}\n")
            f.write(f"Subject: {SUBJECT}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(BODY)
        print("  /home/user/claude-test/email_body.txt")
