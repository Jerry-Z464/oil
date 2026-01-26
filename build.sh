#!/bin/bash

#在终端切换到远程服务器上执行此脚本
#脚本功能：打包并部署到服务器指定位置
#运行方式：./build.sh

# 全局变量
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="OilWell"
SERVICE_NAME="oil.service"
DIST_DIR="${SCRIPT_DIR}/output"
CONFIG_DIR="${SCRIPT_DIR}/config"
TARGET_DIR="/home/edge/server/oil-well"

# 检查依赖
command -v pyinstaller >/dev/null 2>&1 || { echo "错误：PyInstaller 未安装"; exit 1; }

# 2. 打包应用
echo "正在构建 ${APP_NAME}..."
pyinstaller --onefile \
            --distpath "${DIST_DIR}" \
            --workpath "${DIST_DIR}/build" \
            --specpath "${DIST_DIR}" \
            --name "${APP_NAME}" \
            "${SCRIPT_DIR}/setup.py" || { echo "构建失败"; exit 1; }

# 3. 停止服务
echo "正在停止服务..."
sudo systemctl stop "${SERVICE_NAME}" || true

# 4. 部署新版本
echo "正在部署到 ${TARGET_DIR}..."
mkdir -p "${TARGET_DIR}"
cp "${DIST_DIR}/${APP_NAME}" "${TARGET_DIR}/"
cp -r "${CONFIG_DIR}" "${TARGET_DIR}/"

# 5. 重启服务
echo "正在启动服务..."
sudo systemctl daemon-reload
sudo systemctl start "${SERVICE_NAME}" || { echo "服务启动失败"; exit 1; }

echo "部署完成"
