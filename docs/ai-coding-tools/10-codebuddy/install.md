# 📥 安装 CodeBuddy

> CodeBuddy（腾讯云代码助手）是腾讯推出的 AI 编程工具，基于混元代码大模型。

---

## 前置条件

- **Node.js 22+**（检查：`node --version`）
- **Git**（检查：`git --version`）

---

## IDE 版安装

### VS Code

1. 打开 VS Code
2. 点击左侧 **扩展** 图标（或按 `Ctrl + Shift + X`）
3. 搜索 **"CodeBuddy"**
4. 点击 **安装**
5. 重启 VS Code

### JetBrains（IntelliJ IDEA / PyCharm 等）

1. 打开 IDE
2. 菜单 → **Settings** → **Plugins**
3. 搜索 **"CodeBuddy"**
4. 点击 **Install**
5. 重启 IDE

---

## CLI 版安装

### 安装命令

```bash
npm install -g @tencent-ai/codebuddy-code
```

> 💡 如果安装慢，使用国内镜像：
> ```bash
> npm install -g @tencent-ai/codebuddy-code --registry=https://registry.npmmirror.com
> ```

### 验证安装

```bash
codebuddy --version
```

---

## 🔑 登录方式

CodeBuddy CLI 支持 **多种认证方式**：

| 场景 | 推荐方式 | 说明 |
|------|---------|------|
| 个人开发者 | `CODEBUDDY_API_KEY` | 从平台获取 API Key |
| 企业/团队（OAuth） | `apiKeyHelper` | 创建应用获取 Client ID/Secret |
| CI/CD | `CODEBUDDY_AUTH_TOKEN` | 直接使用已有 OAuth token |
| 第三方模型 | `CODEBUDDY_API_KEY` + `BASE_URL` | 使用 OpenRouter 等第三方服务 |

> 优先级：`CODEBUDDY_AUTH_TOKEN` > `apiKeyHelper` > `CODEBUDDY_API_KEY`

---

### 方式一：OAuth 浏览器登录（最简单）

运行 `codebuddy` 命令后会自动打开浏览器完成登录。

```bash
codebuddy
```

登录成功后，CLI 会记住你的登录状态，下次使用不需要重复登录。

> 💡 可以运行 `codebuddy /doctor` 查看当前认证状态和配置信息。

---

### 方式二：API Key 配置

#### Step 1：获取 API Key

| 版本 | 获取地址 |
|------|---------|
| 🌍 海外版 | https://www.codebuddy.ai/profile/keys |
| 🇨🇳 中国版 | https://copilot.tencent.com/profile/ |

#### Step 2：配置环境变量

> ⚠️ **重要**：必须同时配置 `CODEBUDDY_INTERNET_ENVIRONMENT`！这是最常见的配置遗漏。

**🇨🇳 中国版：**

```bash
# macOS / Linux
export CODEBUDDY_API_KEY="你的API-Key"
export CODEBUDDY_INTERNET_ENVIRONMENT=internal
```

```cmd
REM Windows CMD
set CODEBUDDY_API_KEY=你的API-Key
set CODEBUDDY_INTERNET_ENVIRONMENT=internal
```

```powershell
# Windows PowerShell
$env:CODEBUDDY_API_KEY = "你的API-Key"
$env:CODEBUDDY_INTERNET_ENVIRONMENT = "internal"
```

**🌍 海外版：**

```bash
# macOS / Linux
export CODEBUDDY_API_KEY="你的-api-key"
# 海外版无需设置 CODEBUDDY_INTERNET_ENVIRONMENT（默认值）
```

```cmd
REM Windows CMD
set CODEBUDDY_API_KEY=你的-api-key
```

```powershell
# Windows PowerShell
$env:CODEBUDDY_API_KEY = "你的-api-key"
```

| 版本 | `CODEBUDDY_INTERNET_ENVIRONMENT` 值 |
|------|--------------------------------------|
| 🌍 海外版 | 不设置（默认） |
| 🇨🇳 中国版 | `internal` |

> 💡 **持久化**：将环境变量添加到 `~/.bashrc` 或 `~/.zshrc`，避免每次手动设置。

#### Step 3（可选）：在 settings.json 中配置

也可以在 `~/.codebuddy/settings.json` 中配置：

```json
{
  "env": {
    "CODEBUDDY_API_KEY": "你的API-Key",
    "CODEBUDDY_INTERNET_ENVIRONMENT": "internal"
  }
}
```

---

### 方式三：第三方模型服务

```bash
# 使用 OpenRouter 等第三方模型
export CODEBUDDY_API_KEY="sk-or-v1-xxx"
export CODEBUDDY_BASE_URL="https://openrouter.ai/api/v1"
codebuddy --model openai/gpt-4
```

---

## 🩺 诊断命令

遇到问题时运行：

```bash
codebuddy /doctor
```

查看当前配置和连接状态。

---

## 📌 下一步

👉 **[国内版 vs 国际版](./versions.md)**
