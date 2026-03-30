#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
週次ニュースメール スケジューラー
- テスト送信1: 本日 12:50 (15分後)
- テスト送信2: 明日  06:00
"""

import time
import subprocess
import sys
import os
from datetime import datetime, timedelta


def next_target(hour, minute, tomorrow=False):
    now = datetime.now()
    if tomorrow:
        base = (now + timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
    else:
        base = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return base


def wait_and_send(target_dt, label, password):
    now = datetime.now()
    wait_sec = (target_dt - now).total_seconds()
    if wait_sec < 0:
        print(f"[スキップ] {label} の時刻 {target_dt.strftime('%H:%M')} は既に過去です")
        return
    print(f"[待機] {label}: {target_dt.strftime('%Y-%m-%d %H:%M')} まで {int(wait_sec)}秒待機...")
    time.sleep(wait_sec)
    env = os.environ.copy()
    env["SMTP_PASS"] = password
    result = subprocess.run(
        [sys.executable, "/home/user/claude-test/weekly_news_email.py", label],
        env=env,
        capture_output=True,
        text=True
    )
    print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())


if __name__ == "__main__":
    password = os.environ.get("SMTP_PASS", "")
    if not password:
        print("[エラー] SMTP_PASS 環境変数を設定してください")
        sys.exit(1)

    now = datetime.now()
    print(f"=== メールスケジューラー起動 ({now.strftime('%Y-%m-%d %H:%M:%S')}) ===")

    # テスト送信1: 本日 12:50
    t1 = next_target(12, 50, tomorrow=False)
    # テスト送信2: 明日 06:00
    t2 = next_target(6, 0, tomorrow=True)

    print(f"  送信1: {t1.strftime('%Y-%m-%d %H:%M')} [テスト送信1]")
    print(f"  送信2: {t2.strftime('%Y-%m-%d %H:%M')} [テスト送信2]")
    print()

    wait_and_send(t1, "テスト送信1 (本日12:50)", password)
    wait_and_send(t2, "テスト送信2 (明日06:00)", password)

    print("=== スケジューラー完了 ===")
