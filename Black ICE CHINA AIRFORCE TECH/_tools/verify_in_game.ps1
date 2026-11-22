# 中系飞机科技树 —— 游戏内加载校验脚本
#
# 在有交互桌面（已登录、未锁屏）且 Steam 已登录的情况下运行：
#   powershell -ExecutionPolicy Bypass -File _tools\verify_in_game.ps1
#
# 脚本会：
#   1. 备份并临时把本模组加入启用列表
#   2. 通过 Steam 以 -debug_mode 启动 HOI4
#   3. 等待日志写入结束，抓取与本模组相关的报错
#   4. 关闭游戏并还原启用列表
#
# 结果写入 _tools\state\ingame_report.txt

param(
    [string]$ModFile = "blackice_chi_air_tech.mod",
    [int]$TimeoutSec = 900
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$docs = Join-Path $env:USERPROFILE "Documents\Paradox Interactive\Hearts of Iron IV"
$playlist = Join-Path $docs "dlc_load.json"
$logs = Join-Path $docs "logs"
$state = Join-Path $root "_tools\state"
New-Item -ItemType Directory -Force $state | Out-Null
$report = Join-Path $state "ingame_report.txt"

if (-not (Test-Path $playlist)) { throw "找不到 $playlist" }
if (-not (Test-Path (Join-Path $docs "mod\$ModFile"))) { throw "找不到 mod\$ModFile（先运行安装步骤）" }

$backup = Join-Path $state "dlc_load.json.verify_bak"
Copy-Item $playlist $backup -Force

$json = Get-Content $playlist -Raw -Encoding UTF8 | ConvertFrom-Json
if ($json.enabled_mods -notcontains "mod/$ModFile") {
    $json.enabled_mods = @($json.enabled_mods) + "mod/$ModFile"
}
$json | ConvertTo-Json -Depth 4 | Set-Content $playlist -Encoding UTF8
Write-Host "已临时启用 mod/$ModFile"

$errorLog = Join-Path $logs "error.log"
$before = if (Test-Path $errorLog) { (Get-Item $errorLog).Length } else { 0 }
$beforeTime = if (Test-Path $errorLog) { (Get-Item $errorLog).LastWriteTime } else { Get-Date "2000-01-01" }

try {
    Write-Host "启动 HOI4（-debug_mode）……"
    Start-Process "steam://rungameid/394360//-debug_mode"
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    $sawGame = $false
    while ((Get-Date) -lt $deadline) {
        $p = Get-Process hoi4 -ErrorAction SilentlyContinue
        if ($p) { $sawGame = $true }
        if (Test-Path $errorLog) {
            $fi = Get-Item $errorLog
            if ($fi.LastWriteTime -gt $beforeTime -and $fi.Length -gt 0) {
                Start-Sleep -Seconds 25   # 让日志继续写一会儿
                break
            }
        }
        if ($sawGame -and -not $p) { break }   # 进程已退出
        Start-Sleep -Seconds 5
    }
    Start-Sleep -Seconds 3
} finally {
    Write-Host "关闭游戏并还原启用列表……"
    Get-Process hoi4 -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Copy-Item $backup $playlist -Force
}

if (-not (Test-Path $errorLog)) {
    "error.log 不存在：游戏可能未能启动（检查 Steam 是否登录、桌面是否已解锁）" | Set-Content $report -Encoding UTF8
    Write-Host "error.log 不存在，无法校验。" -ForegroundColor Yellow
    exit 1
}

$fi = Get-Item $errorLog
$lines = Get-Content $errorLog -Encoding UTF8
$hits = $lines | Select-String -Pattern 'ad_chi|chinaair|CHI_air' -CaseSensitive:$false

$summary = @()
$summary += "脚本运行时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$summary += "error.log: $($fi.Length) 字节, 最后写入 $($fi.LastWriteTime)"
$summary += "本模组相关行数: $($hits.Count)"
$summary += ""
$summary += "---- 本模组相关日志 ----"
$summary += $hits | ForEach-Object { $_.Line }
$summary += ""
$summary += "---- 需要重点关注的全局报错（grid box / sprite / unknown effect）----"
$summary += $lines | Select-String -Pattern 'Found no grid box|Could not find sprite|Unknown effect|Unknown trigger|Invalid ' |
    Select-Object -Last 40 | ForEach-Object { $_.Line }

$summary | Set-Content $report -Encoding UTF8
Write-Host ""
Get-Content $report -Encoding UTF8 | Select-Object -First 60
Write-Host ""
Write-Host "完整报告: $report"
