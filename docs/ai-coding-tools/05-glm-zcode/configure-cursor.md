# 🖥️ 配置 Cursor 使用 GLM

> 在 Cursor IDE 中使用智谱 GLM 模型，享受 AI 原生编辑器 + 国内最强模型的组合！

---

## 🎯 目标

在 Cursor 中配置 GLM 模型，使用智谱 Coding Plan。

---

## 📋 你需要准备

- [ ] ✅ Cursor 已安装（[下载](https://cursor.com/download)）
- [ ] ✅ 智谱 Coding Plan 已订阅
- [ ] ✅ 智谱 API Key

---

## 🚀 配置步骤

### Step 1：打开 Cursor 设置

1. 启动 Cursor
2. 点击右上角的 **齿轮图标** ⚙️
3. 或者按快捷键 `Ctrl + ,`（Windows/Linux）/ `Cmd + ,`（macOS）

---

### Step 2：找到模型配置

1. 在设置页面，找到 **「Models」** 或 **「模型」** 选项
2. 点击 **「Add Model」** 或 **「添加模型」**

---

### Step 3：配置 OpenAI 兼容端点

智谱 GLM 通过 **OpenAI 兼容格式** 接入 Cursor：

1. 选择模型类型为 **「OpenAI API Key」** 或 **「OpenAI Compatible」**
2. 填写配置：

**🇨🇳 国内版：**

| 配置项 | 填写内容 |
|--------|---------|
| **API Provider** | OpenAI Compatible |
| **Base URL** | `https://open.bigmodel.cn/api/coding/paas/v4` |
| **API Key** | 你的智谱国内版 API Key |
| **Model Name** | `GLM-4.7` |

**🌍 国际版：**

| 配置项 | 填写内容 |
|--------|---------|
| **API Provider** | OpenAI Compatible |
| **Base URL** | `https://api.z.ai/api/coding/paas/v4` |
| **API Key** | 你的智谱国际版 API Key |
| **Model Name** | `GLM-4.7` |

3. 保存配置

> ⚠️ 国内版和国际版的 **API Key 和端点不同**，请根据你订阅的版本选择！

---

### Step 4：选择 GLM 模型

配置完成后：

1. 在 Cursor 的 Chat 或 Composer 界面
2. 点击模型选择下拉框
3. 选择 **GLM-4.7**

现在你可以用 GLM 来编程了！🎉

---

## ✅ 验证

在 Cursor 的 Chat 界面输入：

```
你好，请用一句话介绍你自己
```

如果 GLM 正常回复，说明配置成功！

---

## 💡 使用技巧

### Chat 模式

在 Cursor 中按 `Ctrl + L` 打开 Chat，直接和 GLM 对话。

### Composer 模式

按 `Ctrl + I` 打开 Composer，让 GLM 直接帮你编辑代码。

### Tab 补全

GLM 配置后，Cursor 的代码补全功能也可以使用 GLM 模型。

---

## 📌 下一步

👉 **[专属 MCP 服务器](./mcp-servers.md)**

👉 **[ZCode 编程工具简介](./zcode-intro.md)**
