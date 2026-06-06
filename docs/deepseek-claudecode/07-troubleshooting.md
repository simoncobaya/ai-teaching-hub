# 🔧 常见问题解决

> 遇到问题不要慌！大部分问题都可以在这里找到解决方法。

---

## 📋 目录

- [安装相关问题](#安装相关问题)
- [配置相关问题](#配置相关问题)
- [连接相关问题](#连接相关问题)
- [使用相关问题](#使用相关问题)
- [费用相关问题](#费用相关问题)

---

## 安装相关问题

### ❓ 安装 Claude Code 时报错 "npm ERR!"

**可能原因**：
- Node.js 没有安装或版本太旧
- 网络问题

**解决方法**：

1. 检查 Node.js 版本：
   ```bash
   node --version
   ```
   版本需要 **18 或更高**。如果版本低，去 https://nodejs.org/ 下载最新版。

2. 如果是网络问题，使用国内镜像：
   ```bash
   npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com
   ```

### ❓ 安装 Claude Code 时报错 "EACCES permission denied"

**可能原因**：没有权限安装全局包。

**解决方法**：

**macOS / Linux：**
```bash
sudo npm install -g @anthropic-ai/claude-code
```

**Windows：** 以管理员身份运行 PowerShell，然后再安装。

---

## 配置相关问题

### ❓ settings.json 在哪里？

| 系统 | 路径 |
|------|------|
| Windows | `C:\Users\你的用户名\.claude\settings.json` |
| macOS | `~/.claude/settings.json` |
| Linux | `~/.claude/settings.json` |

> 💡 Windows 上 `.claude` 是隐藏文件夹。在文件管理器的地址栏输入 `%USERPROFILE%\.claude` 可以直接打开。

### ❓ settings.json 格式错误

**症状**：Claude Code 启动报错或无法读取配置。

**检查方法**：

1. 确认 JSON 格式正确（可以用 https://jsonlint.com/ 验证）
2. 常见错误：
   - 最后一个元素后面有多余的逗号 `,`
   - 缺少引号 `"`
   - 缺少大括号 `}`

**正确的格式示例**（使用 `env` 方式）：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-你的DeepSeek-API-Key",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME": "deepseek-v4-pro",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "deepseek-v4-pro",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "CLAUDE_CODE_EFFORT_LEVEL": "max"
  }
}
```

注意：`env` 对象中最后一个键值对后面 **不能有逗号**。

### ❓ 改了配置但不生效

**解决方法**：
1. 保存文件（Ctrl + S）
2. 完全退出 Claude Code（`/quit`）
3. 重新启动 Claude Code（`claude`）

---

## 连接相关问题

### ❓ "Connection refused" 或 "Network error"

**可能原因**：无法连接到 DeepSeek 的服务器。

**解决方法**：

1. **检查网络**：在浏览器中打开 https://api.deepseek.com/ 看看能不能访问
2. **检查代理**：如果你使用了代理，可能需要配置
3. **检查防火墙**：防火墙可能阻止了 Claude Code 的网络请求

### ❓ "401 Unauthorized"

**可能原因**：API Key 不正确。

**解决方法**：
1. 回到 https://platform.deepseek.com/api_keys
2. 检查 Key 是否正确（注意有没有多余的空格）
3. 如果不确定，创建一个新的 Key
4. 更新 settings.json 中 `ANTHROPIC_AUTH_TOKEN` 的值，或重新设置环境变量

### ❓ "402 Payment Required" 或 "Insufficient balance"

**可能原因**：DeepSeek 账户余额不足。

**解决方法**：
1. 登录 https://platform.deepseek.com/
2. 查看余额
3. 充值（最低 10 元）

### ❓ "429 Too Many Requests"

**可能原因**：请求太频繁了。

**解决方法**：
1. 等一会儿再试
2. 不要发送太大的请求
3. 使用 `/compact` 命令压缩上下文

### ❓ 环境变量方式不生效

**可能原因**：环境变量设置有误。

**解决方法**：
1. 在终端中检查环境变量：
   ```bash
   # macOS / Linux
   echo $ANTHROPIC_BASE_URL
   echo $ANTHROPIC_AUTH_TOKEN

   # Windows CMD
   echo %ANTHROPIC_BASE_URL%
   echo %ANTHROPIC_AUTH_TOKEN%

   # Windows PowerShell
   echo $env:ANTHROPIC_BASE_URL
   echo $env:ANTHROPIC_AUTH_TOKEN
   ```
2. 如果输出为空，说明环境变量没有设置成功
3. 重新设置，或改用 settings.json 方式

---

## 使用相关问题

### ❓ AI 回复的内容质量不好

**可能原因**：提示词不够清晰。

**解决方法**：
1. 使用更具体的描述（参考 [提示词技巧](./04-basics.md)）
2. 提供更多上下文信息
3. 尝试用 `/model opus` 切换到更强的模型层级

### ❓ 对话太长，AI 开始"忘记"前面的内容

**解决方法**：

```
/compact
```

这个命令会让 AI 总结之前的对话，释放空间。

### ❓ 想切换回 Claude 模型

在 **CC Switch** 中启用 Claude Official 供应商，就可以切换回 Claude 了。

> 💡 供应商之间的切换（DeepSeek ↔ Claude）需要在 CC Switch 中操作。Claude Code 的 `/model` 命令只能在 sonnet、opus、haiku 之间切换。

---

## 费用相关问题

### ❓ DeepSeek 要花多少钱？

DeepSeek 的价格非常便宜：

| 项目 | 价格 |
|------|------|
| 输入 | ¥1 / 百万字 |
| 输出 | ¥2 / 百万字 |

**举个例子**：
- 写一个猜数字游戏 → 大约 ¥0.01（1 分钱）
- 做一个完整的小项目 → 大约 ¥0.5-2（5 毛到 2 块）
- 一天的学习和编程 → 大约 ¥1-5（1 到 5 块）

### ❓ 如何查看 DeepSeek 用了多少？

1. 登录 https://platform.deepseek.com/
2. 点击「用量」或「Usage」
3. 可以看到每天用了多少 tokens 和费用

### ❓ 充值最低多少？

DeepSeek 最低充值 **10 元**，对学生来说可以用很久。

---

## 📌 还有问题？

如果以上都没有解决你的问题，可以：

1. 📖 查看 [Claude Code 官方文档](https://code.claude.com/docs/)
2. 📖 查看 [DeepSeek API 文档](https://api-docs.deepseek.com/)
3. 💬 问老师或同学
4. 🔄 试试用 **CC Switch** 重新配置（参考 [配置教程](./05-config.md)）

---

[⬅️ 上一页：验证配置 + 第一个项目](./06-verify.md)
