# 中系飞机科技树 —— 安装到启动器
#
# 作用：
#   1. 在 Workshop 目录下建一个 **ASCII 名称** 的目录联接（游戏对含中文的 mod path 兼容性差）
#   2. 在《钢铁雄心 IV》的 mod 目录写 blackice_chi_air_tech.mod
#
# 用法（普通 PowerShell 即可，建 junction 不需要管理员）：
#   powershell -ExecutionPolicy Bypass -File _tools\install.ps1
#
# 卸载：删掉 mod 目录下的 .mod 文件；不想留联接就 rmdir 掉 chi_air_tech（只删链接，不删本体）。

param(
    [string]$ModRoot = "D:\Steam\steamapps\workshop\content\394360\中系飞机科技树",
    [string]$LinkPath = "D:\Steam\steamapps\workshop\content\394360\chi_air_tech",
    [string]$ModFileName = "blackice_chi_air_tech.mod"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path (Join-Path $ModRoot "descriptor.mod"))) {
    throw "找不到 $ModRoot\descriptor.mod，请确认模组路径"
}

# 1) ASCII 联接
if (Test-Path $LinkPath) {
    $item = Get-Item $LinkPath -Force
    if ($item.LinkType -ne "Junction") {
        Write-Host "[!] $LinkPath 已存在且不是目录联接，跳过创建（请检查是否指错）" -ForegroundColor Yellow
    } else {
        Write-Host "[OK] 目录联接已存在：$LinkPath"
    }
} else {
    New-Item -ItemType Junction -Path $LinkPath -Target $ModRoot | Out-Null
    Write-Host "[OK] 已创建目录联接：$LinkPath -> $ModRoot"
}

# 2) 启动器 .mod
$docs = Join-Path $env:USERPROFILE "Documents\Paradox Interactive\Hearts of Iron IV"
$modDir = Join-Path $docs "mod"
if (-not (Test-Path $modDir)) {
    throw "找不到 $modDir —— 先启动一次游戏/启动器让它生成目录"
}
$modFile = Join-Path $modDir $ModFileName
$content = @'
version="0.1.0"
tags={
	"Technologies"
	"Military"
	"Historical"
}
name="黑冰：中系飞机科技树 Black ICE Chinese Aircraft Tech Tree"
picture="thumbnail.png"
dependencies={
	"Blackice HOI IV TEST"
	"BlackICE Aircraft Designer"
	"黑冰：中国国民革命军坦克科技 Black ICE CHINA TANK TECH"
}
supported_version="1.20.*"
path="__PATH__"
'@
$content = $content.Replace("__PATH__", ($LinkPath -replace '\\', '/'))
Set-Content -Path $modFile -Value $content -Encoding UTF8 -NoNewline
Write-Host "[OK] 已写入 $modFile"

Write-Host ""
Write-Host "下一步：" -ForegroundColor Cyan
Write-Host "  1. 打开启动器 -> 模组，勾选「黑冰：中系飞机科技树」，排在中国坦克科技之后"
Write-Host "  2. 启动游戏后看 logs/system.log 是否有：Active Mod Count: 38 / Active Mod: 黑冰：中系飞机科技树"
Write-Host "  3. 载入中国存档 -> 科技界面 -> 空军栏应出现「中国空军」页"
