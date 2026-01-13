# 使用Node.js构建前端
FROM node:18-alpine as build-stage

WORKDIR /app

# 复制package.json
COPY frontend/package*.json ./

# 安装依赖
RUN npm install --registry=https://registry.npmmirror.com

# 复制源代码
COPY frontend .

# 构建生产版本
RUN npm run build

# 使用Nginx服务
FROM nginx:alpine as production-stage

# 复制构建产物
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制Nginx配置
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
