Write-Host "=== sample-mall 启动脚本 ===" -ForegroundColor Green

# 检查 Python 环境
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未找到 python，请先安装 Python 3" -ForegroundColor Red
    exit 1
}

# 安装依赖
Write-Host "正在安装依赖..." -ForegroundColor Yellow
pip install -r requirements.txt

# 启动应用
Write-Host "启动 Flask 应用 (端口 8080)..." -ForegroundColor Yellow
python app.py
