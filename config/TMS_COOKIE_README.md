# TMS接口Cookie配置说明

## 问题原因
TMS接口返回 "No permission" 错误,说明需要登录认证才能访问。

## 解决方案
需要在浏览器登录TMS系统后,复制Cookie到配置文件。

## 配置步骤

### 1. 登录TMS系统
在浏览器中访问 https://tms.51talk.com 并登录

### 2. 获取Cookie
- **Chrome浏览器**:
  1. 按 F12 打开开发者工具
  2. 切换到 "Network" (网络) 标签
  3. 刷新页面
  4. 点击任意请求
  5. 在右侧 "Headers" 中找到 "Request Headers"
  6. 复制 "Cookie" 字段的完整内容

- **Edge浏览器**: 步骤同Chrome

### 3. 配置Cookie
打开文件 `config/tms_config.json`,将复制的Cookie粘贴进去:

```json
{
  "cookie": "这里粘贴你复制的Cookie内容"
}
```

### 4. 重启后端服务
配置完成后,重启后端服务即可生效。

## Cookie示例格式
```
PHPSESSID=abc123def456; user_id=12345; token=xyz789...
```

## 注意事项
1. Cookie包含敏感信息,不要提交到Git仓库
2. Cookie有过期时间,如果再次出现权限错误,需要重新获取
3. `config/tms_config.json` 已添加到 `.gitignore`,不会被提交

## 验证配置
配置完成后,后端日志会显示:
- 成功: `[步骤2-TMS接口] 已加载Cookie配置`
- 失败: `[步骤2-TMS接口] Cookie未配置,可能导致权限错误`
