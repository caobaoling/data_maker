#!/bin/bash

# 定义日志目录
LOG_DIR="logs"
mkdir -p $LOG_DIR

echo "========================================"
echo "  启动 DataMaker 服务 (后台运行)"
echo "========================================"
echo ""

# 1. 启动后端 Flask
echo "[1/2] 正在启动后端 Flask 服务..."
cd backend
nohup python3 app.py > ../$LOG_DIR/backend.log 2>&1 &
BACKEND_PID=$!
cd ..
echo "后端已启动 (PID: $BACKEND_PID)，日志: $LOG_DIR/backend.log"

# 等待后端启动（可根据实际情况调整秒数）
sleep 2

# 2. 启动前端 Vue
echo "[2/2] 正在启动前端 Vue 开发服务器..."
cd frontend
# 这里根据你之前的需求，添加 --host 和 8500 端口
nohup npm run dev -- --host --port 8500 > ../$LOG_DIR/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo "前端已启动 (PID: $FRONTEND_PID)，日志: $LOG_DIR/frontend.log"

echo ""
echo "========================================"
echo "  所有服务已启动"
echo "========================================"
echo "访问地址："
echo "  前端: http://192.168.24.170:8500"
echo "  后端: http://192.168.24.170:5001"
echo ""
echo "查看日志："
echo "  tail -f $LOG_DIR/backend.log"
echo "  tail -f $LOG_DIR/frontend.log"
echo ""
echo "停止服务请使用: kill $BACKEND_PID $FRONTEND_PID"