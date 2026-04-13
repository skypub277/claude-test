#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
週次ニュースブリーフィング メール送信スクリプト
- 送信元: pubsky@outlook.jp
- 送信先: pubsky@outlook.jp, iam11111234yoshi@gmail.com
- SMTP: smtp-mail.outlook.com:587
- パスワード: 環境変数 SMTP_PASS から取得
"""

import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from datetime import datetime

SMTP_HOST = "smtp-mail.outlook.com"
SMTP_PORT = 587
FROM_ADDRESS = "pubsky@outlook.jp"
TO_ADDRESSES = ["pubsky@outlook.jp", "iam11111234yoshi@gmail.com"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_files(date_str):
    """対象日付のtxt/htmlファイルパスを返す"""
    txt = os.path.join(BASE_DIR, f"briefing_{date_str}.txt")
    html = os.path.join(BASE_DIR, f"briefing_{date_str}.html")
    return txt, html


def build_subject(txt_path):
    """txtファイルの1行目から件名を取得"""
    try:
        with open(txt_path, encoding="utf-8") as f:
            first = f.readline().strip()
        if first.startswith("件名："):
            return first[3:]
    except Exception:
        pass
    return f"【週次ブリーフィング】{datetime.now().strftime('%Y/%m/%d')}"


def send(date_str, password, label=""):
    txt_path, html_path = get_files(date_str)

    if not os.path.exists(txt_path):
        print(f"[エラー] テキストファイルが見つかりません: {txt_path}")
        return False

    subject = build_subject(txt_path)

    with open(txt_path, encoding="utf-8") as f:
        body_text = f.read()

    msg = MIMEMultipart("mixed")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = FROM_ADDRESS
    msg["To"] = ", ".join(TO_ADDRESSES)

    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    if os.path.exists(html_path):
        with open(html_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        fname = os.path.basename(html_path)
        part.add_header("Content-Disposition", f'attachment; filename="{fname}"')
        msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(FROM_ADDRESS, password)
            server.sendmail(FROM_ADDRESS, TO_ADDRESSES, msg.as_string())
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[成功]{' ' + label if label else ''} {ts}")
        print(f"  件名: {subject}")
        print(f"  送信先: {', '.join(TO_ADDRESSES)}")
        print(f"  添付: {os.path.basename(html_path) if os.path.exists(html_path) else 'なし'}")
        return True
    except Exception as e:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[失敗]{' ' + label if label else ''} {ts} : {e}")
        return False


if __name__ == "__main__":
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d")
    label = sys.argv[2] if len(sys.argv) > 2 else ""
    password = os.environ.get("SMTP_PASS", "")

    if not password:
        print("[エラー] 環境変数 SMTP_PASS を設定してください")
        sys.exit(1)

    send(date_str, password, label)
