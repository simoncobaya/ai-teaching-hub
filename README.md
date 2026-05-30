# 魔法错题本 Skill

> 拍照上传试卷 → 自动识别批改 → 生成错题库 → 随时查漏补缺

---

## 📖 详细文档

- **[CLI 使用说明](docs/wrong-answer-book/README.md)** — 命令行版错题管理工具（`wrong_answer_book.py`），上传试卷、查看错题、标记掌握、删除记录。
- **[Web 版使用说明](docs/wrong-answer-book/README_WEB.md)** — 基于 Flask 的 Web 界面（`web_app.py`），通过浏览器直观操作错题库。
- **[🧒 小朋友搭建指南](docs/小朋友搭建指南_魔法错题本.md)** — 给小朋友的引导式对话提示词，复制粘贴就能让 AI 帮你搭出同样的工具。

---

## 安装

将 Skill 复制到 CodeBuddy 的 skills 目录（已安装可跳过）：

```bash
# Linux / macOS
cp -r skills/wrong-answer-book .codebuddy/skills/
```

```powershell
# Windows PowerShell
Copy-Item -Recurse -Path "skills/wrong-answer-book" -Destination ".codebuddy\skills\"
```

```cmd
REM Windows CMD
xcopy /E /I "skills\wrong-answer-book" ".codebuddy\skills\wrong-answer-book"
```

在 CodeBuddy 对话框中确认 Skill 已加载。

> 💡 **懒得自己敲命令？** 把下面这句话复制到 CodeBuddy 对话框，让 AI 帮你搞定：

```
帮我安装当前项目的 wrong-answer-book skill：把 skills/wrong-answer-book 复制到项目的 .codebuddy/skills/ 目录，然后用模板创建 credentials.md 并引导我填写腾讯云 API 密钥。
```

---

## 配置 API 密钥

错题库调用腾讯云 OCR 接口识别试卷，需要填写你自己的 API 密钥。

### 1. 获取密钥

前往 [腾讯云控制台 - API 密钥管理](https://console.cloud.tencent.com/cam/capi)，创建或查看你的 SecretId 和 SecretKey。

> 确保该密钥已授权 OCR 服务（策略：`QcloudOCRFullAccess`）。

### 2. 填写配置

从模板复制一份：

```bash
# Linux / macOS
cp skills/wrong-answer-book/assets/.credentials.md credentials.md
```

```powershell
# Windows PowerShell
Copy-Item -Path "skills/wrong-answer-book/assets/.credentials.md" -Destination "credentials.md"
```

```cmd
REM Windows CMD
copy "skills\wrong-answer-book\assets\.credentials.md" "credentials.md"
```

编辑 `credentials.md`，替换占位符为真实密钥。

`credentials.md` 内容示例：

```
| SecretId  | AKIDxxxxxxxxxxxxxxxxxxxxxxxxxx |
| SecretKey | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
```

> `credentials.md` 已被 `.gitignore` 忽略，不会提交到 Git。

---

## 使用

在 CodeBuddy 对话框中，用 `/wrong-answer-book` 命令或直接说「录入错题」「分析试卷」即可触发。

> 💡 **测试素材**：`artifacts/wrong-answer-book/` 目录中提供了试卷图片素材（6 张 png + 4 张 jpeg），可用于测试录入功能。

### 录入试卷错题

```
/wrong-answer-book  [上传试卷照片]
```

或直接：

```
帮我分析这张语文卷子的错题  [上传图片]
```

Skill 会自动完成：
1. **去重** — 同一张试卷不会重复录入
2. **识别** — 调用腾讯云 API 批改试卷
3. **整理** — 提取错题、分析错误原因、诊断薄弱点
4. **写入** — 生成可读的错题库 Markdown 文件

### 查看错题

```
看看错题库           → 列出所有试卷及错题（含已掌握标记）
看 [1]              → 查看第 1 份试卷的完整错题
看 1.2              → 只看第 1 份试卷的第 2 道错题
语文有多少错题？      → 按科目统计
还有多少没掌握？      → 统计未掌握的错题数
```

### 标记掌握

```
掌握了 1.1          → 标记为 ✅ 已掌握
1.2 还没掌握        → 取消已掌握标记
```

### 删除记录

```
删除 [1]            → 删除整份试卷记录（含图片）
删除 1.2            → 只删除第 1 份中的第 2 个错题
```

---

## 文件说明

```
skills/wrong-answer-book/              ← Skill 定义
├── SKILL.md                            ← 核心流程
├── scripts/
│   └── submit_question_mark.py         ← 腾讯云 API 调用脚本
├── assets/
│   ├── .credentials.md                 ← 密钥模板（可提交 Git）
│   └── wrong-answer-book-template.md   ← 输出格式模板
└── references/
    └── api-spec.md                     ← API 接口规范

credentials.md                          ← 你的真实密钥（gitignored）

wrong-answer-book/                 ← 数据目录
├── .index.json                         ← 去重 + 统计索引
├── images/                             ← 试卷原始图片
└── 错题库_*.md                         ← 生成的错题库文件
```

---

## 示例

### 录入一张试卷

```
用户：/wrong-answer-book [上传三年级语文期中试卷.jpg]

Skill：
  ✅ 错题库已生成：wrong-answer-book/错题库_三年级语文_期中测试题.md

  📊 本次统计：
  - 试卷：三年级语文 期中测试题
  - 错题：2 道 / 共 14 题
  - 薄弱点：汉字拼音拼写、音序查字法

  📈 累计：已录入 1 份卷子，共 2 道错题
```

### 查看错题库

```
用户：看看错题库

Skill：
  📚 错题库 | 共 2 份卷子，11 道错题（3 道已掌握）

  [1] 三年级语文 期中测试题     | 2错/14题（1题已掌握）
      ├─ 1.1 汉字拼音拼写 — zǎo chén
      └─ 1.2 ✅ 音序查字法 — 先查大写字母 [已掌握]

  [2] 英语 反义疑问句练习        | 9错/14题（2题已掌握）
      ├─ 2.1 ✅ 反义疑问句 — 回答 [已掌握]
      ├─ 2.2 反义疑问句 — 回答
      └─ ...
```

### 标记已掌握

掌握某道错题后，标个 ✅ 追踪进度：

```
用户：掌握了 1.1

Skill：
  ✅ 已标记 [1] 中错题 1.1「汉字拼音拼写 — zǎo chén」为已掌握
  📊 [1] 进度：1/2 已掌握
```

如果发现还没真正掌握，也可以取消：

```
用户：1.1 还没掌握

Skill：
  ✅ 已取消 [1] 中 1.1 的已掌握标记
  📊 [1] 进度：0/2 已掌握
```

全部错题都掌握时会有彩蛋 🎉：

```
用户：1.2 已掌握

Skill：
  ✅ 已标记 [1] 中错题 1.2「音序查字法 — 先查大写字母」为已掌握
  📊 [1] 全部错题已掌握！🎉
```

### 删除错题

不需要某道错题时，可以按题号删除：

```
用户：删除 1.2

Skill：
  ✅ 已删除 [1] 中的错题 1.2「音序查字法 — 先查大写字母」
  📊 [1] 剩余 1 道错题
```

### 删除试卷

整份试卷都不需要了？连图片带记录一起清掉：

```
用户：删除 [1]

Skill：
  ⚠️ 确认删除「三年级语文 期中测试题」整份试卷记录？
     （将同时删除错题库文件、试卷图片和索引记录）

  用户：确认

  ✅ 已删除整份试卷「三年级语文 期中测试题」
  📈 累计：剩余 1 份卷子，9 道错题
```

---

## 常见问题

**Q: 上传后提示「认证未配置」？**
A: 检查 `credentials.md` 是否存在且已填入真实密钥（不是 `<YOUR_SECRET_ID>` 占位符）。

**Q: API 返回权限错误？**
A: 在 [CAM 控制台](https://console.cloud.tencent.com/cam) 给对应用户关联 `QcloudOCRFullAccess` 策略。

**Q: 同一张图片可以重复录入吗？**
A: 会通过 MD5 去重，提示已录入。如果确实需要重新录入，选择「覆盖」即可。
