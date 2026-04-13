@echo off
chcp 65001 >nul
setlocal

:: ============================================================
:: 週次ブリーフィング 即時実行バッチ
:: このファイルをダブルクリックして実行してください
:: ============================================================

set BASE=C:\Users\pubsk\Desktop\ニュース
set DATE=2026-04-13
set DSTR=20260413
set RAW=https://raw.githubusercontent.com/skypub277/claude-test/claude/weekly-news-email-5mPqa

echo.
echo ===== 週次ブリーフィング 即時実行 =====
echo.

:: Step 1: フォルダ作成
echo [1/4] フォルダを作成しています...
for %%W in (2026-03-09_週次 2026-03-16_週次 2026-03-23_週次 2026-03-30_週次 2026-04-13_週次) do (
    if not exist "%BASE%\%%W" mkdir "%BASE%\%%W"
)
echo       完了

:: Step 2: ファイルダウンロード
echo [2/4] ブリーフィングファイルをダウンロードしています...
powershell -Command "Invoke-WebRequest '%RAW%/briefing_%DSTR%.txt'  -OutFile '%BASE%\%DATE%_週次\briefing_%DSTR%.txt'  -UseBasicParsing"
powershell -Command "Invoke-WebRequest '%RAW%/briefing_%DSTR%.html' -OutFile '%BASE%\%DATE%_週次\briefing_%DSTR%.html' -UseBasicParsing"
echo       完了

:: Step 3: パスワード入力
echo [3/4] Outlookパスワードを入力してください
set /p SMTP_PASS=パスワード:

:: Step 4: メール送信
echo [4/4] メールを送信しています...
powershell -ExecutionPolicy Bypass -Command ^
  "$from='pubsky@outlook.jp';" ^
  "$to=@('pubsky@outlook.jp','iam11111234yoshi@gmail.com');" ^
  "$pass='%SMTP_PASS%';" ^
  "$txt=Get-Content '%BASE%\%DATE%_週次\briefing_%DSTR%.txt' -Raw -Encoding UTF8;" ^
  "$subj=($txt -split \"`n\")[0] -replace '^件名：','';" ^
  "$cred=New-Object Net.NetworkCredential($from,$pass);" ^
  "$smtp=New-Object Net.Mail.SmtpClient('smtp-mail.outlook.com',587);" ^
  "$smtp.EnableSsl=$true; $smtp.Credentials=$cred; $smtp.Timeout=30000;" ^
  "foreach($addr in $to){" ^
  "  $mail=New-Object Net.Mail.MailMessage;" ^
  "  $mail.From=New-Object Net.Mail.MailAddress($from);" ^
  "  $mail.To.Add($addr);" ^
  "  $mail.Subject=$subj;" ^
  "  $mail.SubjectEncoding=[Text.Encoding]::UTF8;" ^
  "  $mail.Body=$txt;" ^
  "  $mail.BodyEncoding=[Text.Encoding]::UTF8;" ^
  "  $att=New-Object Net.Mail.Attachment('%BASE%\%DATE%_週次\briefing_%DSTR%.html');" ^
  "  $mail.Attachments.Add($att);" ^
  "  try{$smtp.Send($mail); Write-Host '[成功]' $addr -ForegroundColor Green}" ^
  "  catch{Write-Host '[失敗]' $addr $_.Exception.Message -ForegroundColor Red}" ^
  "  $mail.Dispose()}" ^
  "$smtp.Dispose()"

echo.
echo ===== 完了 =====
echo TXT : %BASE%\%DATE%_週次\briefing_%DSTR%.txt
echo HTML: %BASE%\%DATE%_週次\briefing_%DSTR%.html
echo.
pause
