# cocos 工具集说明文档

> 本模块围绕课后推荐题接口，提供数据重置、拉取、整理、总结页提取、掌握度校验等完整工作流。

---

## 目录结构

```
cocos/
├── run_post_class_summary.py       # 一键执行脚本（重置 → 拉取 → 生成总结Excel）
├── reset_mastery.py                # 批量重置知识点掌握度（调接口）
├── fetch_api.py                    # 拉取课后推荐题接口，输出 json 文件
├── get_summary.py                  # 从 json 文件提取总结页数据，生成 Excel
├── extract_json_to_dataframe.py    # 从 json.json 提取题目数据，生成整理报表 Excel
├── verify_mastery.py               # 校验接口返回是否符合掌握度起点规则（主校验脚本）
├── test_701_template.py            # 701课后模版接口JSON结构自动化测试脚本
├── check_701_template.py           # 701课后模版检查脚本
├── 题型定义映射关系.xlsx             # 题型编码 → 中文名称（verify_mastery.py 使用）
├── 需求的对应关系.xlsx               # 知识类型+能力标签+掌握度起点 → 允许题型（verify_mastery.py 使用）
├── GC_L0~L2_有效学习目标.xlsx        # 课型+Level → 有效知识点类型+能力项（verify_mastery.py 使用）
├── 6种课型的接口返回json/            # fetch_api.py 按课型保存的 json 文件目录
└── README.md                       # 本文档
```

---

## 预约ID与课型的对应关系

脚本中硬编码了6种课型的测试预约ID：

| appoint_id | 课型 |
|-----------|------|
| `100` | 阅读 |
| `101` | 词汇 |
| `102` | 字母 |
| `103` | 自拼 |
| `104` | 嘉年华 |
| `105` | 对话 |

---

## 推荐使用流程

### 流程一：一键执行（推荐）

使用 `run_post_class_summary.py` 一键完成"重置掌握度 → 拉取接口 → 生成总结Excel"三步：

```bash
# 全部课型
python cocos/run_post_class_summary.py all moderate_mastery

# 单个课型
python cocos/run_post_class_summary.py 101 moderate_mastery

# 多个课型（逗号分隔）
python cocos/run_post_class_summary.py 100,101,103 moderate_mastery
```

### 流程二：分步手动执行

```
step 1: 运行 reset_mastery.py             → 重置知识点掌握度
step 2: 运行 fetch_api.py                 → 拉取接口，保存 json
step 3: 运行 get_summary.py               → 提取总结页数据生成 Excel
step 4: 运行 extract_json_to_dataframe.py → 整理题目数据生成 Excel（可选）
step 5: 运行 verify_mastery.py            → 校验出题规则是否正确（可选）
```

---

## 脚本详细说明

### 1. `run_post_class_summary.py` — 一键执行脚本

**作用：** 按顺序依次调用 `reset_mastery` → `fetch_api` → `get_summary`，完成一次完整的掌握度测试。

**使用方式：**
```bash
# 必须在项目根目录下运行（不可在 cocos/ 目录内）
python cocos/run_post_class_summary.py <课型参数> <掌握程度>
```

**参数说明：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `<课型参数>` | `all`（全部）或课型ID（单个或逗号分隔） | `all` / `101` / `100,103,105` |
| `<掌握程度>` | mastery 值 | `not_mastered` / `moderate_mastery` / `excellent_mastery` / `perfect_mastery` |

**执行步骤：**
1. 【步骤1】调用 `reset_mastery.run()` 重置指定课型的知识点掌握度
2. 【步骤2】调用 `fetch_api.run()` 拉取接口，保存 JSON 到 `6种课型的接口返回json/`
3. 【步骤3】调用 `get_summary.run()` 从保存的 JSON 中提取总结页数据，生成 Excel

---

### 2. `reset_mastery.py` — 批量重置知识点掌握度

**作用：** 查询指定预约ID下的所有知识点ID，批量调用接口将掌握度设置为目标值。

**使用方式：**
```bash
# 默认重置为 not_mastered
python cocos/reset_mastery.py

# 指定 mastery 值
python cocos/reset_mastery.py moderate_mastery
python cocos/reset_mastery.py excellent_mastery
python cocos/reset_mastery.py perfect_mastery
```

**执行流程：**
1. 查询数据库 `midplatform_user_learning.user_appoint_knowledge_mastery`，获取 `APPOINT_IDS` 对应的所有 `knowledge_id`（最多1000条）
2. 对每个 `knowledge_id` 调用接口，`timestamp` 每次实时取当前毫秒时间戳
3. 打印每条请求结果，最后汇总成功/失败数

**接口信息：**
```
POST http://10.0.18.89:8080/midplatform_user_learning/user_appoint_knowledge_mastery/update_mastery
参数: id=<knowledge_id>&mastery=<mastery>&appkey=java&timestamp=<毫秒时间戳>
```

**可修改配置（脚本顶部）：**
```python
APPOINT_IDS = ['100', '101', '102', '103', '104', '105']  # 需要处理的预约ID
```

**可编程调用：**
```python
import reset_mastery
reset_mastery.run(appoint_ids=['100', '101'], mastery='moderate_mastery')
```

---

### 3. `fetch_api.py` — 拉取课后推荐题接口

**作用：** 根据 `appoint_id` 查询数据库获取 `material_id`，再调用课后推荐题接口，将响应保存为 JSON 文件。

**使用方式：**
```bash
# 传入 mastery 后缀参数，批量拉取全部6种课型
python cocos/fetch_api.py moderate_mastery
```

**执行流程：**
1. 遍历全部6种课型的 `appoint_id`
2. 查询数据库 `user_material_progress`，获取 `material_id`
3. 调用接口拉取课后推荐题数据
4. 保存两份文件：
   - `cocos/json.json`（覆盖写入，供其他脚本使用）
   - `cocos/6种课型的接口返回json/<课型ID><课型名称><suffix>.json`（按课型归档）

**接口信息（线上环境）：**
```
GET http://10.0.18.156:8080/midplatform_user_learning_schedule/api/datasource/post_class_remmment
参数: id=<material_id>&appkey=java&timestamp=<毫秒时间戳>
```

**可编程调用：**
```python
import fetch_api
fetch_api.run(appoint_ids=['100', '101'], suffix='moderate_mastery')
```

---

### 4. `get_summary.py` — 提取总结页数据生成 Excel

**作用：** 读取 `6种课型的接口返回json/` 目录下的 JSON 文件，提取总结页（`SUMMARY_*`、`PRE_POST_SETTLE`）中的知识点数据，生成带颜色分组的 Excel。

**使用方式：**
```bash
# 处理该目录下全部 json 文件
python cocos/get_summary.py

# 只处理指定后缀的 json 文件（如 *moderate_mastery.json）
python cocos/get_summary.py moderate_mastery
```

**输出文件：**
- `cocos/sunchuan_result_<时间戳>.xlsx`（无 suffix 参数）
- `cocos/<suffix>_sunchuan_result_<时间戳>.xlsx`（有 suffix 参数）

**提取的模板类型：**

| template_code | 含义 |
|---|---|
| `SUMMARY_V1` | 非完美总结页 |
| `SUMMARY_V2` | 非完美总结页（v2） |
| `SUMMARY_PERSON` | 个性化总结页 |
| `SUMMARY_PERFECT` | 完美总结页 |
| `PRE_POST_SETTLE` | 结算页 |

**输出列：**

| 列名 | 说明 |
|------|------|
| 文件名 | JSON 文件名（即课型标识） |
| template_code | 模板类型 |
| knowledge_key | 知识点 key |
| knowledge_name | 知识点名称 |
| knowledge_id | 知识点 ID |
| knowledge_type | 知识点类型 |
| OUTPUT-SPEAK | 输出-说 能力掌握等级 |
| INPUT-LISTEN | 输入-听 能力掌握等级 |

**格式特性：** 相同文件名（课型）的行自动填充同一种背景色，便于区分。

**可编程调用：**
```python
import get_summary
get_summary.run(suffix='moderate_mastery')  # 指定后缀
get_summary.run()                            # 全部文件
```

---

### 5. `extract_json_to_dataframe.py` — 生成题目整理报表

**作用：** 读取当前目录下的 `json.json`，提取所有题目的知识点信息，输出带格式的 Excel 表格，便于人工核查接口数据结构。

**使用方式：**
```bash
# 需要在 cocos/ 目录下运行（读取的是当前目录的 json.json）
cd cocos
python extract_json_to_dataframe.py
```

**输出文件：** `整理结果_YYYYMMDD_HHMMSS.xlsx`（保存在当前目录）

**提取内容：** 遍历 `json.json` 的 `res` 数组（跳过 `SUMMARY_V1`、`SUMMARY_PERSON`），对每道题的每个知识点输出一行数据：

| 列名 | 说明 |
|------|------|
| 知识点类型 (point_type_name_en) | 知识点英文类型 |
| 对应能力标签 (ability) | 能力标签编码 |
| 知识点 ID (point_id) | 知识点 ID |
| 题型名称 (question_type_name) | 题型中文名 |
| 题型代码 (question_type) | 题型编码（如 TS_1001） |

**格式特性：** 自动按知识点类型→能力标签→知识点ID 排序，前3列相同内容自动合并单元格，列宽行高自适应。

---

### 6. `verify_mastery.py` — 掌握度起点校验（主校验脚本）

#### 6.1 功能概述

对照数据库中用户的知识点掌握度，验证课后推荐题接口是否按需求规则返回了正确的题型和题数。支持可选的课程范围过滤：当指定课型和 Level 时，仅校验该节课涉及的知识点组合，其余组合自动跳过。

#### 6.2 使用方式

```bash
# 模式一：校验全部知识点（不限课程范围）
python cocos/verify_mastery.py <appoint_id>

# 模式二：仅校验指定课型和 Level 涉及的知识点
python cocos/verify_mastery.py <appoint_id> <课型-en> <Level>
```

**参数说明：**

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `appoint_id` | 是 | 预约 ID | `100` |
| `<课型-en>` | 否 | 课型英文名，与 `GC_L0~L2_有效学习目标.xlsx` 中"课型-en"列完全一致 | `reading_class` |
| `<Level>` | 否（与课型同时提供） | Level，与 xlsx 中"Level"列完全一致 | `Level 2` |

**课型-en 可选值：**

| 课型-en | 中文名 |
|---------|--------|
| `vocabulary_class` | 词汇句型课 |
| `conversation_class` | 对话课 |
| `reading_class` | 阅读课 |
| `alphabet_class` | 字母课 |
| `phonics_class` | 自拼课 |
| `carnival_class` | 嘉年华 |

**Level 可选值：** `Level 0`、`Level 1`、`Level 2`

**示例：**
```bash
python cocos/verify_mastery.py 100 reading_class "Level 2"
python cocos/verify_mastery.py 100
```

**脚本顶部常量（IDE 中直接运行时使用）：**
```python
APPOINT_ID   = '100'
LESSON_TYPE  = 'reading_class'  # 留空 '' 则不过滤
LESSON_LEVEL = 'Level 2'        # 留空 '' 则不过滤
```

#### 6.3 数据来源

| 来源 | 说明 |
|------|------|
| 数据库 | `midplatform_user_learning.user_appoint_knowledge_mastery`（用户知识点掌握度） |
| 接口数据 | `json.json`（接口实际返回的题目，由 `fetch_api.py` 生成） |
| 题型映射 | `题型定义映射关系.xlsx`（题型编码 → 中文名） |
| 需求规则 | `需求的对应关系.xlsx`（知识类型+能力标签+起点 → 允许题型） |
| 课程范围 | `GC_L0~L2_有效学习目标.xlsx`（课型+Level → 知识点类型+能力项组合） |

脚本执行时会**自动调用 `fetch_api.fetch()` 拉取最新接口数据**，无需手动执行 `fetch_api.py`。

#### 6.4 核心数据映射

**掌握度数值映射（DB 字段值 → 数字）：**

| DB 字段值 | 数字 | 含义 |
|-----------|------|------|
| `not_mastered` | 1 | 未掌握 |
| `moderate_mastery` | 2 | 中等掌握 |
| `excellent_mastery` | 3 | 良好掌握 |
| `perfect_mastery` | 4 | 完全掌握，接口不返回该知识点 |

**知识类型映射（DB 英文 → 需求文档中文）：**

| DB 英文值 | 中文 |
|-----------|------|
| `word_sense` / `phrase_sense` | 词汇 |
| `sentence` / `sentence_pattern_structure` | 句型 |
| `alphabet_rule` | 字母 |
| `phonics_rule` | 自然拼读 |
| `conversation` | 对话 |
| `reading` | 阅读 |

**能力标签映射（DB 英文 → 需求文档中文）：**

| DB 英文值 | 中文 |
|-----------|------|
| `INPUT-LISTEN` | 输入-听 |
| `OUTPUT-SPEAK` | 输出-说 |
| `INTERACTION-SPEAK` | 交际-说 |
| `PHONICS-READ` | 自拼-认读 |

#### 6.5 校验规则详解

校验的核心单位是**分组**：将同一（知识类型中文, 能力标签中文）下的所有知识点归为一组，整组统一校验。

##### 知识点个数 = 1

逐层过滤：从该知识点的掌握度起始层开始遍历到 mastery=3，若过滤掉低层已用题型后仍有可用题型，则该层期望出 1 道题。

**校验内容：**
- 实际返回题数是否等于期望题数
- 实际返回题型是否在允许范围内

##### 知识点个数 > 1（分层校验）

以 **mastery=3 层是否含连线题** 为分支：

**分支A：mastery=3 有连线题**
- mastery=1/2 层：按分支B方式出非连线题（每知识点1题，逐层过滤已用题型）
- mastery=3 层：出连线题（按知识点数区间计算道数）

**分支B：mastery=3 无连线题**
- 按 mastery=1 → mastery=2 → mastery=3 顺序出题
- 每层过滤掉前面所有层已用题型，同层统一选1种题型，每个知识点各1题

**mastery=3 连线题道数规则（分支A）：**

| 参与知识点数 N | 期望连线题道数 |
|--------------|-------------|
| 2 ≤ N ≤ 4 | 1道 |
| 5 ≤ N ≤ 8 | 2道 |
| 9 ≤ N ≤ 12 | 3道 |

> 连线类题型：`图音连线`、`图图连线`、`图音连线3-3`、`图图连线3-3`

**mastery=4：** 接口不应返回该组任何题目。

#### 6.6 接口忽略的模板类型

以下 `template_code` 为非题目模板，校验时自动跳过：

| template_code | 含义 |
|---|---|
| `SUMMARY_V1` | 非完美总结页 |
| `SUMMARY_V2` | 非完美总结页（v2） |
| `SUMMARY_PERSON` | 个性化总结页 |
| `SUMMARY_PERFECT` | 完美总结页 |
| `PRE_POST_SETTLE` | 结算页 |

#### 6.7 校验输出示例

```
========================================================================
  掌握度起点校验报告（按知识点分组）
========================================================================
  [本节课范围] 共 3 组 知识点类型+能力项：
    point_type=reading | ability=INPUT-LISTEN
    point_type=reading | ability=OUTPUT-SPEAK
    point_type=reading_content | ability=INPUT-LISTEN

  [跳过] 接口返回但不在本节课范围内，共 2 组（不参与校验）：
    point_type=word_sense | ability=INPUT-LISTEN | 题数=5

  ── 分组: knowledge_type=阅读(['reading']) | ability=输入-听(['INPUT-LISTEN'])
     知识点个数=3 | 最低mastery=1
       knowledge_id=2070028239241567 | reading | INPUT-LISTEN | mastery=1
       knowledge_id=2070028239241562 | reading | INPUT-LISTEN | mastery=1
       knowledge_id=2070028239241563 | reading | INPUT-LISTEN | mastery=2
     [通过] 知识点=3 | 期望7道，实际返回7道
            期望层级: mastery=1: [TS_1001(听音选图)] → 3道（每知识点1题） | mastery=2: [TS_1005(图文选音)] → 3道（每知识点1题） | mastery=3(连线题优先): [TS_2001(图音连线)] → 1道
            实际返回:
              TS_1001(听音选图) kids=['2070028239241567']
              ...

  ── 分组: knowledge_type=阅读(['reading']) | ability=输入-听(['INPUT-LISTEN'])
     知识点个数=2 | 最低mastery=4
     [通过] mastery=4，接口未返回（符合需求）

------------------------------------------------------------------------
  汇总：通过=3  失败=0  跳过=0
------------------------------------------------------------------------
========================================================================
```

#### 6.8 脚本内部函数说明

| 函数 | 说明 |
|------|------|
| `load_question_type_map()` | 读取题型编码↔中文名双向映射 |
| `load_requirement_rules()` | 读取需求对应关系，处理合并单元格和 `--` |
| `load_db_mastery(appoint_id)` | 从数据库查询指定预约 ID 的知识点掌握度列表 |
| `load_api_questions(json_file)` | 解析 `json.json`，提取题目信息，跳过非题目模板 |
| `load_lesson_scope(lesson_type_en, level)` | 从 `GC_L0~L2_有效学习目标.xlsx` 读取课型+Level 对应的知识点类型+能力项组合 |
| `_calc_expected_lianxian(n)` | 计算 mastery=3 层连线题期望道数 |
| `verify(...)` | 核心校验函数，按分组逐一校验并打印报告 |

---

### 7. `test_701_template.py` — 701课后模版接口JSON结构测试

**作用：** 对课后模版接口返回的 JSON 数据进行自动化结构校验，覆盖6种课型的5种 Template 规范，生成带颜色标注的 Excel 测试报告。

**测试用例覆盖：**

| TC | Template | 校验内容 |
|---|---|---|
| TC-01 | `SUMMARY_PERFECT` | 全掌握场景（100/102/105）：video必须是有效URL，title/good/need等字段必须为null |
| TC-02 | `SUMMARY_V1` | 词汇课（101）/ 自拼课（103）：words/phonics结构、ability_level值范围[1-4] |
| TC-03 | `SUMMARY_V2` | 嘉年华（104）：Lv0有letters、Lv1~2有phonics，video有效 |
| TC-04 | `SUMMARY_PERSON` | 个性化汇总：固定标题文案、good/need列表、audio字段存在性 |
| TC-05 | `PRE_POST_SETTLE` | 结尾帧：`data` 必须为 null |
| TC-06 | 整体响应 | `code=="10000"`、`message=="success"`、`res`非空、`PRE_POST_SETTLE`在最后 |
| TC-07 | 掌握度对应 | excellent→good_performance有数据；not_mastered→need_strengthen有数据 |

**使用方式：**
```bash
# 测试单个JSON文件
python cocos/test_701_template.py path/to/xxx.json

# 测试目录下所有json文件
python cocos/test_701_template.py "cocos/6种课型的接口返回json/"

# 手动指定掌握度（不从文件名推断）
python cocos/test_701_template.py xxx.json --mastery excellent

# 指定报告输出目录
python cocos/test_701_template.py xxx.json --output ./reports
```

**参数说明：**

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `target` | 是 | JSON文件路径或包含JSON文件的目录 | `xxx.json` / `6种课型的接口返回json/` |
| `--mastery` | 否 | 手动指定掌握度（不指定则从文件名关键字推断） | `excellent` / `moderate` / `not_mastered` |
| `--output` | 否 | 报告输出目录，默认当前目录 | `./reports` |

**掌握度自动推断规则（从文件名关键字）：**

| 文件名含关键字 | 推断掌握度 |
|---|---|
| `excellent` | excellent |
| `not_mastered` / `not mastered` | not_mastered |
| `moderate` | moderate |

**输出结果：**
- **控制台**：每条检查项实时打印 `√ PASS` / `× FAIL` / `! WARN`
- **Excel报告**：自动生成 `test_701_result_YYYYMMDD_HHMMSS.xlsx`，绿/红/黄色标注结果，包含"测试文件/Template/检查项/结果/说明"五列
- **退出码**：有 FAIL 则 `exit(1)`，否则 `exit(0)`（可集成到 CI）

---

## 依赖说明

| 依赖包 | 用途 |
|--------|------|
| `requests` | HTTP 请求 |
| `pandas` | DataFrame 处理 |
| `openpyxl` | Excel 读写与格式化 |
| `pymysql` | 数据库查询 |

```bash
pip install requests pandas openpyxl pymysql
```

---

## 常见问题

**Q: `fetch_api.py` 提示变量 `appoint_id` 未定义？**

当前 `fetch_api.py` 的 `__main__` 块存在 `appoint_id` 未赋值的问题，请通过 `run_post_class_summary.py` 调用，或直接调用 `fetch_api.run()` 函数。

**Q: `extract_json_to_dataframe.py` 找不到 `json.json`？**

该脚本读取的是**当前工作目录**下的 `json.json`，需要先 `cd cocos` 再执行，或先运行 `fetch_api.py` 生成 `json.json`。

**Q: `verify_mastery.py` 找不到某课型/Level 的有效学习目标？**

检查 `GC_L0~L2_有效学习目标.xlsx` 的"课型-en"列是否与传参完全一致（区分大小写）。可用值见 [6.2 使用方式](#62-使用方式) 中的课型-en 表格。
