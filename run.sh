#!/bin/bash

# 定义日志目录
LOG_DIR="logs"
mkdir -p $LOG_DIR

echo "========================================"
echo "  启动 DataMaker 服务 (后台运行)"
echo "========================================"

# 1. 启动后端 Flask
echo "[1/2] 正在启动后端 Flask 服务..."
cd backend
# 清除旧的 PID 文件（如果有）
[ -f backend.pid ] && rm backend.pid
nohup python3 app.py > ../$LOG_DIR/backend.log 2>&1 &
echo $! > ../backend.pid  # 将 PID 保存到上一级目录
cd ..
echo "后端已启动 (PID: $(cat backend.pid))"

# 2. 启动前端 Vue
echo "[2/2] 正在启动前端 Vue 开发服务器..."
cd frontend
# 清除旧的 PID 文件（如果有）
[ -f frontend.pid ] && rm frontend.pid
nohup npm run dev -- --host --port 8500 > ../$LOG_DIR/frontend.log 2>&1 &
echo $! > ../frontend.pid # 将 PID 保存到上一级目录
cd ..
echo "前端已启动 (PID: $(cat frontend.pid))"


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