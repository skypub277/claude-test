# ============================================================
# 週次ブリーフィング 完全実行スクリプト（Windows用）
# 実行: PowerShell を管理者として実行 → .\run_briefing.ps1
# ============================================================

param(
    [string]$SmtpPass = $env:SMTP_PASS,
    [string]$DateStr  = (Get-Date -Format "yyyyMMdd"),
    [switch]$SetupScheduler
)

$BASE     = "C:\Users\pubsk\Desktop\ニュース"
$DATE_DIR = "$(Get-Date -Format 'yyyy-MM-dd')_週次"
$WEEK_DIR = Join-Path $BASE $DATE_DIR
$TXT      = Join-Path $WEEK_DIR "briefing_$DateStr.txt"
$HTML_SRC = Join-Path $PSScriptRoot "briefing_$DateStr.html"
$HTML_DST = Join-Path $WEEK_DIR "briefing_$DateStr.html"
$FROM     = "pubsky@outlook.jp"
$TO       = @("pubsky@outlook.jp","iam11111234yoshi@gmail.com")
$SMTP     = "smtp-mail.outlook.com"
$PORT     = 587

# ── Step 1: フォルダ作成 ──────────────────────────────────
Write-Host "`n[Step 1] フォルダ作成" -ForegroundColor Cyan
$weeks = @("2026-03-09_週次","2026-03-16_週次","2026-03-23_週次","2026-03-30_週次","2026-04-13_週次")
foreach ($w in $weeks) {
    $p = Join-Path $BASE $w
    if (-not (Test-Path $p)) { New-Item -ItemType Directory -Path $p -Force | Out-Null; Write-Host "  [作成] $p" }
    else { Write-Host "  [既存] $p" -ForegroundColor Gray }
}

# ── Step 2: HTMLをコピー ──────────────────────────────────
Write-Host "`n[Step 2] HTMLファイルをコピー" -ForegroundColor Cyan
if (Test-Path $HTML_SRC) {
    Copy-Item $HTML_SRC $HTML_DST -Force
    Write-Host "  [コピー] $HTML_DST" -ForegroundColor Green
} else {
    Write-Host "  [スキップ] HTMLファイルが見つかりません: $HTML_SRC" -ForegroundColor Yellow
}

# ── Step 3: TXTファイルの確認 ────────────────────────────
Write-Host "`n[Step 3] ブリーフィングTXTの確認" -ForegroundColor Cyan
if (-not (Test-Path $TXT)) {
    Write-Host "  [エラー] TXTファイルが見つかりません: $TXT" -ForegroundColor Red
    Write-Host "  GitリポジトリからTXTファイルをコピーしてください"
    exit 1
}
Write-Host "  [OK] $TXT" -ForegroundColor Green

# ── Step 4: メール送信 ────────────────────────────────────
Write-Host "`n[Step 4] メール送信" -ForegroundColor Cyan

if (-not $SmtpPass) {
    $SecPass  = Read-Host "Outlookパスワードを入力してください" -AsSecureString
    $SmtpPass = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
                    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecPass))
}

$body    = Get-Content $TXT -Raw -Encoding UTF8
$subject = ($body -split "`n")[0] -replace "^件名：",""

$cred = New-Object System.Net.NetworkCredential($FROM, $SmtpPass)
$smtp = New-Object System.Net.Mail.SmtpClient($SMTP, $PORT)
$smtp.EnableSsl            = $true
$smtp.Credentials          = $cred
$smtp.DeliveryMethod       = [System.Net.Mail.SmtpDeliveryMethod]::Network
$smtp.Timeout              = 30000

foreach ($to in $TO) {
    try {
        $mail            = New-Object System.Net.Mail.MailMessage
        $mail.From       = New-Object System.Net.Mail.MailAddress($FROM)
        $mail.To.Add($to)
        $mail.Subject    = $subject
        $mail.Body       = $body
        $mail.BodyEncoding = [System.Text.Encoding]::UTF8
        $mail.SubjectEncoding = [System.Text.Encoding]::UTF8
        if (Test-Path $HTML_DST) {
            $att = New-Object System.Net.Mail.Attachment($HTML_DST)
            $mail.Attachments.Add($att)
        }
        $smtp.Send($mail)
        Write-Host "  [成功] $to" -ForegroundColor Green
        $mail.Dispose()
    } catch {
        Write-Host "  [失敗] ${to}: $_" -ForegroundColor Red
    }
}
$smtp.Dispose()

# ── Step 5: タスクスケジューラー登録（初回のみ）──────────
if ($SetupScheduler) {
    Write-Host "`n[Step 5] タスクスケジューラー登録" -ForegroundColor Cyan
    $ps   = "powershell.exe"
    $args = "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
    $log  = Join-Path $BASE "scheduler.log"

    $action = New-ScheduledTaskAction -Execute $ps -Argument $args
    $trigMon = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "06:00"
    $trigFri = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At "06:00"

    Register-ScheduledTask -TaskName "週次ブリーフィング_月曜" `
        -Action $action -Trigger $trigMon -RunLevel Highest -Force | Out-Null
    Register-ScheduledTask -TaskName "週次ブリーフィング_金曜" `
        -Action $action -Trigger $trigFri -RunLevel Highest -Force | Out-Null

    Write-Host "  [登録] 毎週月曜 06:00 / 金曜 06:00" -ForegroundColor Green
}

Write-Host "`n===== 完了 =====" -ForegroundColor Cyan
Write-Host "  TXT: $TXT"
Write-Host "  HTML: $HTML_DST"
Write-Host "  送信先: $($TO -join ' / ')"
