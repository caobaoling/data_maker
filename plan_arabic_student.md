# Plan

在 DataMaker 平台的"用户管理"菜单下添加"阿语学员"功能，用于在测试环境下给学员添加/查询阿语标签。通过调用 51talk 的 Admin 接口实现。

## Scope
- In:
  - 后端：新增阿语标签管理 API（查询、添加标签）
  - 前端：新增"阿语学员"页面组件
  - 路由：注册新页面路由和菜单项
  - 类型支持：ar_tea（阿语意向）、ar_point（已付费阿语订单）
- Out:
  - 不涉及生产环境接口调用
  - 不修改现有用户财富功能

## Action items
[ ] 在 `backend/api/user.py` 中添加阿语标签查询和添加的 API 端点
[ ] 在 `frontend/src/api/user.js` 中添加对应的前端 API 调用方法
[ ] 创建 `frontend/src/views/user/ArabicStudent.vue` 页面组件
[ ] 在 `frontend/src/router/index.js` 中添加"/user/arabic-student"路由
[ ] 在 `frontend/src/layout/MainLayout.vue` 的"用户管理"菜单下添加"阿语学员"菜单项
[ ] 验证接口调用格式（user_id 参数、type 类型、action 参数）
[ ] 本地测试功能是否正常

## Open questions
- 调用 51talk 接口是否需要特殊的 cookie 或认证信息？
- 接口返回的数据格式是什么？需要确认后做相应解析
