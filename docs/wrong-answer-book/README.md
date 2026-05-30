# 魔法错题本 — CLI 使用说明

`wrong_answer_book.py` 是命令行版错题管理工具，上传试卷照片后自动调用腾讯云 OCR API 识别批改，提取错题生成 Markdown 错题库，支持查看、标记掌握、删除和统计。

## 环境要求

- Python 3.8+
- 腾讯云 OCR 服务 SecretId / SecretKey

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

```bash
# 1. 初始化工作目录
python wrong_answer_book.py init

# 2. 编辑 credentials.md，填入腾讯云密钥
#    SecretId  / SecretKey

# 3. 上传试卷
python wrong_answer_book.py analyze ./试卷.jpg --subject 语文 --grade 三年级 --exam 期中测试

# 4. 查看错题
python wrong_answer_book.py list
```

## 命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `init` | 初始化工作目录，创建目录结构和 credentials 模板 | `python wrong_answer_book.py init` |
| `analyze` | 上传试卷图片，自动识别批改并生成错题库 | `python wrong_answer_book.py analyze ./试卷.jpg --subject 语文 --grade 三年级 --exam 期中测试` |
| `list` | 层级化列出所有错题（试卷 → 单题） | `python wrong_answer_book.py list` |
| `view` | 查看试卷全文或单题详情 | `python wrong_answer_book.py view 1` 或 `view 1.2` |
| `stats` | 统计查询，支持按科目/年级过滤 | `python wrong_answer_book.py stats --subject 语文` |
| `master` | 标记错题为已掌握 | `python wrong_answer_book.py master 1.2` |
| `unmaster` | 取消错题的已掌握标记 | `python wrong_answer_book.py unmaster 1.2` |
| `delete` | 删除整份试卷或单个错题 | `python wrong_answer_book.py delete 1` 或 `delete 1.2` |
| `help` | 显示总览或单条命令的详细帮助 | `python wrong_answer_book.py help analyze` |

### 通用参数

| 参数 | 说明 |
|------|------|
| `-d, --work-dir` | 指定工作目录（默认为当前目录） |

---

### `init` — 初始化

```bash
python wrong_answer_book.py init [--force]
```

| 选项 | 说明 |
|------|------|
| `--force` | 强制覆盖已有模板（不会覆盖已有数据） |

执行后会在工作目录下创建：
```
wrong-answer-book/
├── .index.json        # 索引文件
└── images/            # 试卷图片存储

credentials.md         # 腾讯云密钥模板（编辑后填入真实密钥）
```

---

### `analyze` — 分析试卷

```bash
python wrong_answer_book.py analyze <图片路径> [--subject 科目] [--grade 年级] [--exam 试卷名]
```

| 参数 | 说明 |
|------|------|
| `image` | 试卷图片路径（必填，支持 jpg/png/webp/bmp） |
| `--subject` | 科目（选填，如：语文、数学、英语） |
| `--grade` | 年级（选填，如：三年级、七年级） |
| `--exam` | 试卷名称（选填，如：期中测试题） |

**分析流程**（最多等待 120 秒）：
1. 校验图片格式和大小（≤10MB）
2. 计算 MD5 指纹，检查是否重复录入
3. 保存图片到 `images/` 目录
4. 调用腾讯云 OCR 批改 API
5. 解析错题并推断科目/年级（如未提供）
6. 生成 Markdown 错题库文件
7. 更新索引

如果检测到重复试卷会提示是否覆盖；若未提供科目和年级，工具会自动从试卷内容推断。

---

### `list` — 列出错题

```bash
python wrong_answer_book.py list [--flat]
```

| 选项 | 说明 |
|------|------|
| `--flat` | 简洁模式，不展开每道错题的详细信息 |

以层级结构展示：

```
📚 错题库 | 共 2 份卷子，5 道错题（2 道已掌握）

[1] 三年级语文 期中测试 | 2026-05-30 | 3错/14题 （1题已掌握）
    ├─ 1.1 ❌ 看拼音写词语 — (3)那个小女孩...
    ├─ 1.2 ❌ 音序查字法 — 准:用音序查字法...

[2] 三年级数学 单元测试 | 2026-05-28 | 2错/10题
    ├─ 2.1 ✅ 乘除法混合运算 — 125×8÷4=...
```

编号规则：`N.M`，N 为试卷序号（从 1 开始），M 为该试卷内的错题序号。

---

### `view` — 查看详情

```bash
python wrong_answer_book.py view <编号>
```

| 编号格式 | 含义 | 示例 |
|----------|------|------|
| `N` | 查看整份试卷的 Markdown 全文 | `view 1` |
| `N.M` | 查看单个错题的详细信息 | `view 1.2` |

单题详情输出示例：

```
--- [1] 三年级语文 期中测试 | 3错/14题 ---

### 1.2 — 音序查字法

大题：(五)按查字典的知识填空。(7分)
答错空：准:用音序查字法，先查大写字母

| 我的答案 | Z |
| 正确答案 | ZH |
| 错误原因 | 音序查字法应先查大写字母并写出完整音节 |
```

---

### `stats` — 统计查询

```bash
python wrong_answer_book.py stats [--subject 科目] [--grade 年级]
```

输出总览 + 按科目/年级分组统计：

```
📊 错题统计

   试卷数：2 份
   总题数：24 道
   错题数：5 道
   已掌握：2 道
   未掌握：3 道
   掌握率：40%

按科目：
   语文: 3 错（1 已掌握）
   数学: 2 错（1 已掌握）

按年级：
   三年级: 5 错（2 已掌握）
```

---

### `master` / `unmaster` — 掌握标记

```bash
python wrong_answer_book.py master 1.2     # 标记为已掌握
python wrong_answer_book.py unmaster 1.2   # 取消掌握标记
```

标记后自动更新 Markdown 表格状态列和索引，输出当前试卷的掌握进度。

---

### `delete` — 删除

```bash
python wrong_answer_book.py delete 1       # 删除整份试卷
python wrong_answer_book.py delete 1.2     # 删除单个错题
```

删除前会要求输入 `y` 确认。删除试卷会同时清除 .md 文件、图片和索引；删除单题会重新编号后续错题并更新统计。

---

### `help` — 查看帮助

```bash
python wrong_answer_book.py help           # 命令总览
python wrong_answer_book.py help analyze   # 查看 analyze 命令详细用法
```

---

## 工作目录结构

```
work-dir/
├── wrong_answer_book.py       # 本工具
├── requirements.txt           # Python 依赖
├── credentials.md             # 腾讯云密钥（不纳入版本控制）
└── wrong-answer-book/         # 数据目录
    ├── .index.json            # 索引文件（JSON 数组）
    ├── 错题库_三年级语文_期中测试.md
    ├── 错题库_三年级数学_单元测试.md
    └── images/                # 试卷原图
        ├── 01adb08c...jpeg
        └── ...
```

### 索引文件格式 (`.index.json`)

```json
[
  {
    "md5": "01adb08c6d6bb4695dc53ce16ca71a3f",
    "image": "images/01adb08c...jpeg",
    "file": "错题库_三年级语文_期中测试.md",
    "subject": "语文",
    "grade": "三年级",
    "exam_name": "期中测试",
    "wrong_count": 3,
    "total_questions": 14,
    "mastered": [2],
    "created_at": "2026-05-30T09:00:00"
  }
]
```

## 注意事项

1. **密钥安全**：`credentials.md` 包含腾讯云 SecretId/SecretKey，请勿提交到 Git（已在 `.gitignore` 中排除）
2. **文件大小**：图片上限 10MB，支持 jpg/png/webp/bmp 格式
3. **API 超时**：批改任务最长等待 120 秒，超时会报错
4. **重复检测**：同一张图片（相同 MD5）不会重复录入，可选覆盖
5. **科目推断**：如不指定 `--subject`，工具会根据题目关键词自动推断，准确性有限
