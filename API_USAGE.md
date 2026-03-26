# 预约API使用说明

## 📌 重要变更

### 旧版本 (已废弃)
```javascript
// 普通话预约
addAppointCn(data)  // POST /api/appoint/add_cn

// 英语预约
addAppointEn(data)  // POST /api/appoint/add_en
```

### 新版本 (推荐)
```javascript
// 统一接口,支持所有课程类型
addAppoint(data)  // POST /api/appoint/add
```

## 🚀 使用方式

### 1. 前端调用示例

```javascript
import { addAppoint } from '@/api/appoint'

// 添加普通话预约
const data = {
  course_type: '31',  // 关键参数
  stu_id: '12345678',
  t_id: '350012781',
  start_time: '2026-01-15 10:00:00',
  end_time: '2026-01-15 10:30:00',
  date_time: '20260115_20',
  use_point: 'buy',
  level_id: '1400011',
  unit_id: '1406021',
  course_id: '1406031'
}

const result = await addAppoint(data)
```

### 2. 课程类型配置

后端会根据 `course_type` 参数自动应用对应配置:

| 课程类型 | course_type | point_type | category | 说明 |
|---------|------------|------------|----------|------|
| 普通话 | '31' | pthpoint | ph_buy/ph_free | 中文课程 |
| 英语 | '1' | point | ph_buy/ph_free | 英语课程 |
| 阿语 | '39' | ar_point | unkown | 阿拉伯语课程 |

### 3. 完整请求参数

```javascript
{
  // ===== 必填参数 =====
  course_type: '31',     // 课程类型(31=普通话, 1=英语, 39=阿语)
  stu_id: '12345678',    // 学生ID
  t_id: '350012781',     // 教师ID
  start_time: '2026-01-15 10:00:00',  // 开始时间
  end_time: '2026-01-15 10:30:00',    // 结束时间
  date_time: '20260115_20',           // 时间编号
  course_id: '1406031',  // 三级教材ID
  level_id: '1400011',   // 一级教材ID
  unit_id: '1406021',    // 二级教材ID

  // ===== 可选参数 =====
  use_point: 'buy',      // 课程性质(buy=付费课, free=体验课)
  status: 'on',          // 预约状态(on=正常, cancel=取消)
  cost_num: 1,           // 消耗数量
  point_type: '',        // 财富类型(留空则自动计算)
  category: ''           // 课程种类(留空则自动计算)
}
```

## 🔧 后端处理流程

1. **接收请求** → 解析 `course_type` 参数
2. **配置映射** → 根据课程类型加载对应配置
3. **参数计算** → 自动计算 time, date, category 等
4. **调用外部API** → 创建预约
5. **数据同步** → 同步到 `teanew.appoint_aggregation` 和 `talk.appoint`

## ✅ 兼容性

旧版本的函数仍然可用,但内部已统一为新接口:

```javascript
// 这两种写法效果相同
addAppointCn(data)  // 内部调用 addAppoint(data)
addAppointEn(data)  // 内部调用 addAppoint(data)
addAppoint(data)    // 推荐使用
```

## 📊 数据同步

预约成功后,数据会自动同步到以下表:

1. **talkplatform_appoint_reconstruction.appoint** (主表)
2. **teanew.appoint_aggregation** (聚合表,额外字段: is_overseas, extra)
3. **talk.appoint** (旧系统兼容表)

## 🎯 代码优势

### 优化前
- 3个独立的接口 (`/add_cn`, `/add_en`, `/add_ar`)
- 代码重复,维护困难
- 前端需要判断调用哪个接口

### 优化后
- 1个统一接口 (`/add`)
- 配置化管理,易于扩展
- 前端只需传递 `course_type`,后端自动处理

## 📝 测试建议

### 测试普通话预约
```bash
curl -X POST http://localhost:3000/api/appoint/add \
  -H "Content-Type: application/json" \
  -d '{
    "course_type": "31",
    "stu_id": "12345678",
    "t_id": "350012781",
    ...
  }'
```

### 测试英语预约
```bash
curl -X POST http://localhost:3000/api/appoint/add \
  -H "Content-Type: application/json" \
  -d '{
    "course_type": "1",
    "stu_id": "12345678",
    "t_id": "2821",
    ...
  }'
```

### 测试阿语预约
```bash
curl -X POST http://localhost:3000/api/appoint/add \
  -H "Content-Type: application/json" \
  -d '{
    "course_type": "39",
    "stu_id": "12345678",
    "t_id": "360107171",
    ...
  }'
```

## ⚠️ 注意事项

1. **course_type 必填** - 这是后端识别课程类型的关键参数
2. **时间格式** - 统一使用 `YYYY-MM-DD HH:mm:ss` 格式
3. **教材ID** - 不同课程类型使用不同的默认教材ID
4. **数据同步** - 如果同步失败,主流程仍然成功,会记录警告日志

## 🔍 故障排查

### 前端添加失败
1. 检查 `course_type` 参数是否正确传递
2. 查看浏览器控制台网络请求
3. 确认请求URL是 `/api/appoint/add`

### 后端错误
1. 查看后端日志输出
2. 检查数据库连接
3. 验证外部API是否可访问

### 数据同步失败
1. 检查数据库权限
2. 查看同步日志
3. 手动验证目标表是否存在
