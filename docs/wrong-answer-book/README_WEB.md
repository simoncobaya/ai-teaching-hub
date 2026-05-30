# 魔法错题本 — Web 版使用说明

`web_app.py` 是基于 Flask 的 Web 界面，让小朋友通过浏览器直观操作错题库，所有业务逻辑复用 `wrong_answer_book.py`。

## 环境要求

- Python 3.8+
- 已初始化的 CLI 工作目录（含 `credentials.md`）

## 安装

```bash
# 从项目目录
cd app/wrong-answer-book
pip install -r requirements.txt
```

## 启动

```bash
python web_app.py
```

默认在 `http://127.0.0.1:5000` 启动，只绑定本地地址。

### 启动选项

```bash
python web_app.py --port 8080                          # 自定义端口
python web_app.py --work-dir /home/user/my-wab         # 指定工作目录
python web_app.py --host 0.0.0.0 --port 8080           # 局域网内访问（谨慎）
python web_app.py --debug                               # 调试模式（自动重载）
```

---

## 界面导览

打开浏览器访问首页后，你会看到：

### 🏠 统计横幅

顶端四张彩色卡片展示全局统计：
- 📋 **试卷数** — 已录入的试卷份数
- ❌ **错题数** — 全部错题总数
- ✅ **已掌握** — 标记为掌握的错题数
- 🎯 **掌握率** — 已掌握占比百分比

### ➕ 上传试卷

点击紫色大按钮 **「➕ 上传新试卷」** 弹出上传表单：

1. 点击虚线框选择试卷照片（或拖拽）
2. 选填科目、年级、试卷名称（不填也会自动推断）
3. 点击 **「开始分析」** 提交任务
4. 看到 🔍 加载动画和进度提示
5. 完成后自动刷新列表，Toast 提示结果

分析在后台线程执行，最长等待 120 秒，前端每 2.5 秒轮询一次状态。

### 📋 试卷卡片列表

每张卡片显示一份试卷：

- **左侧图标**：科目相关 emoji（📖语文 / 🧮数学 / 🔤英语）
- **居中信息**：年级科目、考试名、录入日期、总题数
- **右侧进度条**：绿色 = 已掌握，橙色底 = 未掌握，显示 `X/Y 已掌握`
- **底部操作**：展开/收起按钮、删除试卷按钮、加油/庆祝提示

点击卡片标题可展开/收起单题列表。

### 📝 错题列表

展开卡片后看到每道错题：

- 圆形序号（橙色=未掌握，绿色=已掌握）
- 大题名称 + 小题描述 + 知识点标签
- 右侧 **「标记掌握」** / **「✅ 已掌握」** 切换按钮

点击错题标题打开右侧 **详情抽屉**。

### 🔍 详情抽屉

从右侧滑入的面板，展示单题完整信息：

| 字段 | 说明 |
|------|------|
| 📖 试卷 | 所属试卷信息 |
| 📌 大题 | 大题题号与标题 |
| 📄 原题 | 题目原文（如有） |
| ✏️ 答错空 | 具体答错的小题 |
| ❌ 我的答案 | 手写作答内容（红边） |
| ✅ 正确答案 | 标准答案（绿边） |
| 💡 错误原因 | API 分析返回的错误原因 |
| 底部按钮 | 切换掌握状态 |

点击遮罩层或按 `Esc` 关闭。

### 📊 统计弹窗

导航栏 **「📊 统计」** 按钮打开统计弹窗，包含：

- 总览数值
- 按科目分组（含进度条）
- 按年级分组（含进度条）

### 🗑️ 删除确认

点击试卷卡片底部 **「🗑️ 删除试卷」** 弹出确认弹窗，防止误删。

---

## API 参考

所有 API 返回统一 JSON 格式：

```json
// 成功
{ "ok": true, "data": { ... } }

// 失败
{ "ok": false, "error": "错误描述" }
```

| 方法 | 路由 | 说明 |
|------|------|------|
| `GET` | `/` | 前端页面 |
| `GET` | `/api/init-status` | 检查是否已初始化 |
| `POST` | `/api/init` | 初始化工作目录 |
| `POST` | `/api/analyze` | 提交试卷分析（multipart form） |
| `GET` | `/api/task/<id>` | 查询分析任务状态 |
| `GET` | `/api/records` | 获取所有错题记录 |
| `GET` | `/api/view/<ref>` | 查看试卷或单题详情 |
| `GET` | `/api/stats` | 统计数据 |
| `POST` | `/api/master/<ref>` | 标记掌握 |
| `POST` | `/api/unmaster/<ref>` | 取消掌握 |
| `DELETE` | `/api/delete/<ref>` | 删除记录 |
| `GET` | `/images/<filename>` | 试卷图片文件 |

### POST /api/analyze

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -F "image=@试卷.jpg" \
  -F "subject=语文" \
  -F "grade=三年级" \
  -F "exam_name=期中测试"
```

返回 `{ "ok": true, "data": { "task_id": "a1b2c3d4e5f6" } }`，然后用任务 ID 轮询：

```bash
curl http://127.0.0.1:5000/api/task/a1b2c3d4e5f6
```

任务状态：

| status | 含义 |
|--------|------|
| `submitted` | 已创建，等待开始 |
| `running` | 正在执行（`progress` 字段含当前步骤） |
| `done` | 完成（`result` 字段含结果摘要） |
| `failed` | 失败（`error` 字段含错误信息） |

### GET /api/records

```json
{
  "ok": true,
  "data": [
    {
      "num": 1,
      "subject": "语文",
      "grade": "三年级",
      "exam_name": "期中测试",
      "wrong_count": 2,
      "total_questions": 14,
      "mastered": [1],
      "mastered_count": 1,
      "created_at": "2026-05-30T09:00:00",
      "image": "images/01adb08c.jpeg",
      "wrong_items": [
        {
          "seq": 1,
          "big_question": "(一)根据语境拼写词语",
          "sub_question": "(3)那个小女孩把双手拢...",
          "knowledge_points": "看拼音写词语",
          "mastered": true
        },
        {
          "seq": 2,
          "big_question": "(五)按查字典的知识填空",
          "sub_question": "准:用音序查字法...",
          "knowledge_points": "音序查字法",
          "mastered": false
        }
      ]
    }
  ]
}
```

---

## 设计说明

- **单用户设计**：任务状态存储在内存 `dict` 中，重启后未完成的任务丢失（不影响已入库数据）
- **本地绑定**：默认 `127.0.0.1` 仅本机访问，如有需要绑定 `0.0.0.0` 请注意网络安全
- **无数据库依赖**：所有数据存储在 `.index.json` 和 `.md` 文件中，可直接在文件管理器中查看
- **小朋友友好**：大字体、圆角卡片、emoji 图标、柔和配色、按钮放大动画
