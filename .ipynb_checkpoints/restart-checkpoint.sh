#!/bin/bash

echo "========================================"
echo "  重启 DataMaker 服务"
echo "========================================"

# 定义关闭函数
kill_process() {
    PID_FILE=$1
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo "正在终止进程 (PID: $PID)..."
            kill -9 "$PID"
            rm "$PID_FILE"
            echo "进程已终止。"
        else
            echo "PID $PID 对应的进程不存在，清理残留文件。"
            rm "$PID_FILE"
        fi
    else
        echo "未找到 $PID_FILE，跳过。"
    fi
}

echo "[1/2] 正在清理旧进程..."
kill_process "backend.pid"
kill_process "frontend.pid"

echo ""
echo "[2/2] 正在重新启动服务..."
# 调用 start.sh
bash start.sh

echo "重启完成。"