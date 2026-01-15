# 🐳 Docker 部署指南

## 📋 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- 系统: Windows/macOS/Linux

---

## 🚀 快速启动

### 1. 一键启动所有服务

```bash
# 构建并启动（后台运行）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看实时日志
docker-compose logs -f
```

### 2. 访问应用

- **前端界面**: http://localhost:8080
- **后端API**: http://localhost:5001/api/health
- **健康检查**: http://localhost:5001/api/health

---

## 🔧 常用命令

### 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose stop

# 重启服务
docker-compose restart

# 停止并删除容器
docker-compose down

# 停止并删除容器+卷+镜像
docker-compose down -v --rmi all
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs

# 实时查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend

# 查看最近50行日志
docker-compose logs --tail=50 backend
```

### 服务状态

```bash
# 查看运行中的容器
docker-compose ps

# 查看容器详细信息
docker-compose ps -a

# 查看资源使用情况
docker stats
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入前端容器
docker-compose exec frontend sh

# 以root身份进入
docker-compose exec -u root backend bash
```

---

## 🔄 更新和重建

### 代码更新后重建

```bash
# 方式一：重新构建所有服务
docker-compose up -d --build

# 方式二：仅重建特定服务
docker-compose up -d --build backend
docker-compose up -d --build frontend

# 方式三：完全清理后重建
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 更新镜像

```bash
# 拉取最新镜像
docker-compose pull

# 重启服务使用新镜像
docker-compose up -d
```

---

## 🛠️ 故障排查

### 1. 端口被占用

**问题**: 端口5001或8080已被占用

**解决方案**:

修改 `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "5002:5001"  # 改为5002

  frontend:
    ports:
      - "8081:80"    # 改为8081
```

### 2. 构建失败

**问题**: 网络超时或依赖安装失败

**解决方案**:

```bash
# 使用国内镜像源重新构建
docker-compose build --no-cache

# 查看构建日志
docker-compose build --progress=plain
```

### 3. 容器无法启动

**问题**: 容器启动后立即退出

**排查步骤**:

```bash
# 查看容器退出原因
docker-compose ps -a

# 查看容器日志
docker-compose logs backend

# 查看Docker守护进程日志
# Windows: Docker Desktop -> Troubleshoot -> View logs
# Linux: journalctl -u docker
```

### 4. 服务无法访问

**问题**: 浏览器无法访问8080端口

**排查步骤**:

```bash
# 1. 确认容器运行状态
docker-compose ps

# 2. 确认端口映射
docker-compose port frontend 80

# 3. 检查容器日志
docker-compose logs frontend

# 4. 测试容器内部
docker-compose exec frontend wget -O- http://localhost:80
```

### 5. 数据库连接失败

**问题**: 后端无法连接数据库

**解决方案**:

1. 检查 `config/database.json` 配置
2. 确认数据库IP可访问
3. 测试网络连通性:

```bash
docker-compose exec backend ping 172.16.70.20
```

---

## 📊 性能优化

### 资源限制

在 `docker-compose.yml` 中添加资源限制:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          memory: 256M
```

### 减少镜像大小

使用多阶段构建（已应用）:

- 前端: Node构建阶段 + Nginx运行阶段
- 后端: Python slim镜像

### 清理未使用资源

```bash
# 清理停止的容器
docker container prune

# 清理未使用的镜像
docker image prune -a

# 清理未使用的卷
docker volume prune

# 清理所有未使用资源
docker system prune -a --volumes
```

---

## 🔐 安全配置

### 生产环境建议

1. **修改默认端口**:
```yaml
ports:
  - "127.0.0.1:5001:5001"  # 仅监听本地
```

2. **使用环境变量**:
```yaml
environment:
  - DB_HOST=${DB_HOST}
  - DB_PASSWORD=${DB_PASSWORD}
```

3. **限制容器权限**:
```yaml
security_opt:
  - no-new-privileges:true
read_only: true
```

4. **定期更新基础镜像**:
```bash
docker-compose pull
docker-compose up -d
```

---

## 📁 数据持久化

### 挂载配置文件

当前配置（已生效）:

```yaml
volumes:
  - ./common:/app/common      # 公共模块
  - ./config:/app/config      # 配置文件
```

### 添加数据卷

如需持久化数据，可添加:

```yaml
volumes:
  datamaker-data:
    driver: local

services:
  backend:
    volumes:
      - datamaker-data:/app/data
```

---

## 🌐 网络配置

### 自定义网络

当前配置:

```yaml
networks:
  datamaker-network:
    driver: bridge
```

### 服务间通信

容器可通过服务名互相访问:

- 前端访问后端: `http://backend:5001`
- 后端内部: `http://localhost:5001`

### 外部网络访问

如需连接外部服务:

```yaml
networks:
  default:
    external:
      name: external_network
```

---

## 📝 Docker Compose 完整配置

当前生效的配置:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: datamaker-backend
    ports:
      - "5001:5001"
    volumes:
      - ./common:/app/common
      - ./config:/app/config
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    networks:
      - datamaker-network

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    container_name: datamaker-frontend
    ports:
      - "8080:80"
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - datamaker-network

networks:
  datamaker-network:
    driver: bridge
```

---

## 🧪 测试和验证

### 健康检查

```bash
# 后端健康检查
curl http://localhost:5001/api/health

# 前端访问测试
curl http://localhost:8080

# 测试API端点
curl http://localhost:8080/api/health
```

### 容器内测试

```bash
# 测试后端Flask应用
docker-compose exec backend python -c "import app; print('OK')"

# 测试前端Nginx
docker-compose exec frontend nginx -t
```

---

## 📚 参考资料

- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose文档](https://docs.docker.com/compose/)
- [Dockerfile最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

## 🆘 获取帮助

遇到问题？

1. 查看日志: `docker-compose logs -f`
2. 检查网络: `docker-compose ps`
3. 重启服务: `docker-compose restart`
4. 提交Issue: https://github.com/caobaoling/data_maker/issues

---

<div align="center">

**🐳 Docker让部署更简单！**

</div>
