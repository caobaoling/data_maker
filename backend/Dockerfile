# 使用Python 3.11官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制requirements.txt
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制后端代码
COPY backend /app/backend

# 复制公共模块和配置
COPY common /app/common
COPY config /app/config

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV PYTHONPATH=/app/backend
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# 启动命令 (使用gunicorn生产服务器)
WORKDIR /app/backend
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
