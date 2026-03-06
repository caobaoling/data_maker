@echo off
echo ========================================
echo   启动 DataMaker 服务
echo ========================================
echo.

echo [1/2] 启动后端 Flask 服务...
start "Flask Backend" cmd /k "cd backend && python app.py"
timeout /t 2 /nobreak >nul

echo [2/2] 启动前端 Vue 开发服务器...
start "Vue Frontend" cmd /k "cd frontend && npm run dev -- --host"

echo.
echo ========================================
echo   服务启动完成！
echo ========================================
echo.
echo 访问地址：
echo   前端: http://172.16.116.181:3000
echo   后端: http://172.16.116.181:5001
echo.
echo 按任意键关闭此窗口...
pause >nul
