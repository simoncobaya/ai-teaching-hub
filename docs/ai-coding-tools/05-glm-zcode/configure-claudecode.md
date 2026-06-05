# 🤖 配置 Claude Code 使用 GLM

> 让 Claude Code 使用智谱 GLM 模型，有两种方式：Anthropic 兼容模式和 OpenAI 兼容模式。

---

## 🎯 目标

配置 Claude Code，使其可以通过智谱 Coding Plan 使用 GLM 模型。

---

## 📋 你需要准备

- [ ] ✅ 智谱 Coding Plan 已订阅
- [ ] ✅ 智谱 API Key 已获取
- [ ] ✅ Claude Code 已安装

---

## 🚀 配置方式

### 🌟 方式一：自动化工具（最简单）

智谱提供了一键配置工具：

```bash
npx @z_ai/coding-helper
```

运行后按提示操作，自动完成所有配置！

---

### 方式二：自动化脚本（Mac/Linux）

在终端中运行：

```bash
curl -O "https://cdn.bigmodel.cn/install/claude_code_env.sh" && bash ./claude_code_env.sh
```

脚本会自动帮你配置环境变量。

---

### 方式三：手动配置 settings.json（通用）

编辑 `~/.claude/settings.json`，添加智谱的配置：

**🇨🇳 国内版（bigmodel.cn）：**

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "你的智谱国内版API-Key",
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

**🌍 国际版（z.ai）：**

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "你的智谱国际版API-Key",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

> 💡 **注意**：国内版和国际版使用 **不同的 API 端点** 和 **不同的 API Key**，请根据你订阅的版本选择对应的配置。
>
> 智谱使用的是 **Anthropic 兼容端点**，配置中用的是 `ANTHROPIC_AUTH_TOKEN` 而不是 `ANTHROPIC_API_KEY`。

---

### 方式四：用 CC Switch 配置

如果你已经安装了 CC Switch：

1. 打开 CC Switch
2. 添加供应商 → 选择 **「ZhipuAI / GLM」** 预设
3. 填入智谱 API Key
4. Base URL 会自动设置为 `https://open.bigmodel.cn/api/anthropic`
5. 选择目标工具（Claude Code）
6. 保存并启用

> 👉 详见 [CC Switch 教程](../04-cc-switch/add-provider.md)

---

## ✅ 验证配置

1. 退出并重启 Claude Code
2. 启动后发送一条测试消息：
   ```
   你好，请告诉我你是什么模型
   ```
3. 如果 GLM 正常回复，说明配置成功！🎉

---

## 🔄 在 DeepSeek 和 GLM 之间切换

如果你同时配置了 DeepSeek 和 GLM，可以随时切换：

### 使用环境变量方式

修改 `~/.claude/settings.json`：

**切换到 GLM：**
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "你的智谱API-Key",
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic"
  }
}
```

**切换到 DeepSeek：**
```json
{
  "providers": [
    {
      "name": "deepseek",
      "baseURL": "https://api.deepseek.com",
      "apiKey": "你的DeepSeek-API-Key",
      "models": [{"id": "deepseek-chat", "name": "deepseek"}]
    }
  ]
}
```

### 使用 CC Switch（推荐）

用 CC Switch 一键切换，不需要手动改文件！

---

## 📊 GLM vs DeepSeek 怎么选？

| 维度 | GLM | DeepSeek |
|------|-----|----------|
| 计费方式 | 月费订阅（不限量） | 按 token 付费 |
| 中文能力 | ⭐⭐⭐⭐⭐ 特别好 | ⭐⭐⭐⭐ 很好 |
| 编程能力 | ⭐⭐⭐⭐⭐ 强 | ⭐⭐⭐⭐⭐ 强 |
| 适合场景 | 经常编程、不限量 | 偶尔使用、按量付费 |
| 专属 MCP | ✅ 视觉/搜索/GitHub | ❌ 无 |

> 💡 **建议**：两个都配置上，日常用 DeepSeek（便宜），需要中文特别好或 MCP 功能时切换到 GLM。

---

## ❓ 常见问题

### Q：配置后 Claude Code 报错 "API error"？

检查以下几点：
1. API Key 是否正确（有没有多余空格）
2. Base URL 是否正确：`https://open.bigmodel.cn/api/anthropic`
3. Coding Plan 是否还有效

### Q：GLM 和 DeepSeek 可以同时配置吗？

可以！使用 CC Switch 最方便，也可以在 settings.json 中同时配置 providers（DeepSeek）和 env（GLM）。但注意 env 方式会影响默认行为，建议用 CC Switch 切换。

---

## 📌 下一步

👉 **[配置 Cursor 使用 GLM](./configure-cursor.md)**

👉 **[专属 MCP 服务器](./mcp-servers.md)**

👉 **[ZCode 编程工具简介](./zcode-intro.md)**
