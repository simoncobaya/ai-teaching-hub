# 🐋 配置 Cursor 使用 DeepSeek

> Cursor 默认使用自己的 AI 模型，但你也可以配置 DeepSeek 来省钱！

---

## 🎯 目标

在 Cursor 中配置 DeepSeek 作为 AI 模型。

---

## 🚀 配置步骤

### Step 1：打开模型设置

1. 打开 Cursor
2. 点击右上角 **齿轮图标** ⚙️ → **Settings**
3. 找到 **「Models」** 部分

---

### Step 2：添加 OpenAI 兼容模型

1. 点击 **「Add Model」**
2. 在模型名称中输入：`deepseek-chat`
3. 找到 **「OpenAI API Key」** 设置区域

---

### Step 3：配置 API

在 OpenAI API Key 设置区域：

| 配置项 | 填写内容 |
|--------|---------|
| **API Key** | 你的 DeepSeek API Key |
| **Base URL** | `https://api.deepseek.com/v1` |

> 💡 把 Base URL 改成 DeepSeek 的地址，API Key 填你的 DeepSeek Key。

---

### Step 4：选择 DeepSeek 模型

配置完成后：

1. 在 Chat 或 Composer 界面
2. 点击模型选择下拉框
3. 选择 **deepseek-chat**

现在 Cursor 使用的是 DeepSeek 模型了！🎉

---

## ✅ 验证

在 Cursor Chat 中输入：

```
你好，请告诉我你是什么模型
```

如果 DeepSeek 正常回复（通常会提到 DeepSeek），说明配置成功！

---

## 🔄 切换模型

在 Cursor 中随时可以切换模型：

- 选择 **deepseek-chat** → 使用 DeepSeek（便宜）
- 选择 **claude-3.5-sonnet** → 使用 Cursor 内置 Claude（Pro 用户）
- 选择 **gpt-4o** → 使用 Cursor 内置 GPT-4（Pro 用户）

> 💡 **建议**：日常用 DeepSeek 省钱，复杂任务切换到更强的模型。

---

## 💰 费用说明

| 模型 | 费用 |
|------|------|
| Cursor 内置模型 | 消耗 Cursor 额度（免费版有次数限制） |
| DeepSeek（自定义） | 消耗 DeepSeek 余额（很便宜） |

使用自定义 DeepSeek 模型 **不消耗** Cursor 的免费额度！

---

## 📌 下一步

👉 **[OpenAI Codex](../07-codex/README.md)**

👉 **[工具对比](../99-comparison/README.md)**
