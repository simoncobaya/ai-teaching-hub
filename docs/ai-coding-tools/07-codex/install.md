# 📥 安装 Codex CLI

---

## 一键安装（推荐）

### macOS / Linux

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

### Windows

打开 PowerShell，运行：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

---

## 其他安装方式

### npm

```bash
npm install -g @openai/codex
```

> 💡 需要 Node.js 22 或更高版本（检查：`node --version`）

### Homebrew（macOS）

```bash
brew install --cask codex
```

### 国内镜像（npm）

```bash
npm install -g @openai/codex --registry=https://registry.npmmirror.com
```

### 直接下载二进制文件

前往 [GitHub Releases](https://github.com/openai/codex/releases) 下载对应平台的版本：

| 平台 | 文件名 |
|------|--------|
| macOS Apple Silicon | `codex-aarch64-apple-darwin.tar.gz` |
| macOS Intel | `codex-x86_64-apple-darwin.tar.gz` |
| Linux x86_64 | `codex-x86_64-unknown-linux-musl.tar.gz` |
| Linux ARM64 | `codex-aarch64-unknown-linux-musl.tar.gz` |
| Windows x86_64 | `codex-x86_64-pc-windows-msvc.exe.zip` |
| Windows ARM64 | `codex-aarch64-pc-windows-msvc.exe.zip` |

下载后解压，建议重命名为 `codex` 方便使用。

---

## 🔑 登录认证

安装完成后运行 `codex`，有两种认证方式：

> 💰 **费用说明**：Codex CLI 本身免费开源！但使用时需要 OpenAI API 额度（按用量付费）或 ChatGPT 订阅（Plus $20/月）。如果不想付费，可以看看 [OpenCode](../08-opencode/README.md) 等免费替代方案。

### 方式一：ChatGPT 账号登录（推荐 ✅）

```bash
codex
```

启动后选择 **Sign in with ChatGPT**，用你的 ChatGPT 账号登录即可。

> 💡 支持 ChatGPT Plus、Pro、Business、Edu、Enterprise 订阅计划。

### 方式二：API Key

```bash
# macOS / Linux
export OPENAI_API_KEY="sk-your-openai-api-key"

# Windows PowerShell
$env:OPENAI_API_KEY = "sk-your-openai-api-key"
```

---

## ✅ 验证安装

```bash
codex --version
```

显示版本号即安装成功！🎉

---

## 📌 下一步

👉 **[基础用法](./basics.md)** — 学会怎么用 Codex CLI
