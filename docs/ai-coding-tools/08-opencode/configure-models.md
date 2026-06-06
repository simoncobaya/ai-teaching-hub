# 🔌 配置各种模型

> OpenCode 支持连接任何 AI 模型！教你配置 DeepSeek、GLM 等。

---

## 配置方式

OpenCode 通过配置文件或环境变量来连接 AI 模型。

---

## 🐋 配置 DeepSeek

### 环境变量方式

```bash
export OPENAI_API_KEY="你的DeepSeek-API-Key"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"
```

### 配置文件方式

编辑 OpenCode 的配置文件，添加：

```json
{
  "provider": "openai",
  "model": "deepseek-v4-flash",
  "apiKey": "你的DeepSeek-API-Key",
  "baseURL": "https://api.deepseek.com/v1"
}
```

---

## 🧠 配置智谱 GLM

```bash
export OPENAI_API_KEY="你的智谱-API-Key"
export OPENAI_BASE_URL="https://open.bigmodel.cn/api/coding/paas/v4"
```

模型名使用 `GLM-4.7`。

---

## 🤖 配置 Claude

```bash
export ANTHROPIC_API_KEY="你的Anthropic-API-Key"
```

模型选择 `claude-sonnet-4-6`。

---

## 🆓 配置免费模型

### Gemini（Google 免费模型）

```bash
export GEMINI_API_KEY="你的Gemini-API-Key"
```

### Ollama（本地模型，完全离线）

1. 安装 Ollama：https://ollama.com/
2. 下载模型：`ollama pull codellama`
3. OpenCode 配置使用 Ollama

> 💡 Ollama 完全免费，但需要较好的电脑配置。

---

## 用 CC Switch 配置（最简单）

如果你安装了 CC Switch，可以直接在 CC Switch 中配置 OpenCode：

1. 打开 CC Switch
2. 找到 OpenCode
3. 选择供应商和模型
4. 保存

👉 详见 [CC Switch 教程](../04-cc-switch/README.md)

---

## 📌 下一步

👉 **[TRAE IDE](../09-trae/README.md)** — 有免费额度，体验顶级模型

👉 **[工具对比](../99-comparison/README.md)**
