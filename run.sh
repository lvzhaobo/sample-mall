#!/bin/bash

echo "=== sample-mall 启动脚本 ==="

# 检查 Python 环境
if ! command -v python3 &> /dev/null
then
    echo "错误: 未找到 python3，请先安装 Python 3"
    exit 1
fi

# 安装依赖
echo "正在安装依赖..."
pip3 install -r requirements.txt

# 启动应用
echo "启动 Flask 应用 (端口 8080)..."
python3 app.py
