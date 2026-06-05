# ✅ 验证配置是否成功

> 配置完成后，先验证一下是否成功！

---

## 🎯 目标

确认 Claude Code 已经成功连接到 DeepSeek。

---

## 🚀 验证步骤

### Step 1：启动 Claude Code

打开终端，进入你的项目文件夹，启动 Claude Code：

```bash
cd my-first-project
claude
```

---

### Step 2：检查当前模型

在 Claude Code 中输入：

```
/model
```

你会看到当前可用的模型层级。如果配置成功，你可以看到 sonnet、opus、haiku 等选项（配置了 DeepSeek 后，这些模型实际调用的就是 DeepSeek）。

---

### Step 3：发送测试消息

输入一个简单的问题：

```
你好！请用一句话介绍你自己，并告诉我你是哪个模型。
```

**期望结果**：

- ✅ 如果 DeepSeek 回复了（通常会提到自己是 DeepSeek），说明 **配置成功**！🎉
- ❌ 如果报错了，请看下面的 [故障排除](#故障排除)

---

### Step 4：测试编程能力

试试让 DeepSeek 写一小段代码：

```
帮我写一个 Python 函数，输入两个数字，返回它们的和。
```

如果 DeepSeek 成功帮你写出了代码，说明一切正常！

---

## 🎉 验证成功！

恭喜你！Claude Code + DeepSeek 配置成功！🎊

你现在拥有了一个：
- 💰 便宜的 AI 编程助手（DeepSeek 超便宜）
- 🧠 聪明的编程能力（DeepSeek 编程能力很强）
- 🇨🇳 中文理解好（DeepSeek 对中文很友好）
- 🔄 可以在 CC Switch 中随时切换供应商（DeepSeek ↔ Claude）

---

## 🐛 故障排除

### 问题 1：连接失败 / 超时

**可能原因**：网络问题

**解决方法**：
1. 检查网络连接是否正常
2. 如果在国内，可能需要配置网络代理
3. 试试直接访问 https://api.deepseek.com/ 看看能不能打开

### 问题 2：API Key 无效

**可能原因**：API Key 错误或过期

**解决方法**：
1. 回到 DeepSeek 平台：https://platform.deepseek.com/api_keys
2. 检查 API Key 是否正确
3. 如果不确定，重新创建一个新的 Key
4. 更新配置中的 API Key

### 问题 3：余额不足

**可能原因**：DeepSeek 账户没有余额了

**解决方法**：
1. 登录 DeepSeek 平台：https://platform.deepseek.com/
2. 查看余额
3. 如果余额不足，充值（最低 10 元）

### 问题 4：模型列表里没有 DeepSeek

**可能原因**：配置没有生效

**解决方法**：
1. 检查 `settings.json` 文件内容是否正确
2. 确认 JSON 格式没有错误
3. 退出 Claude Code，重新启动

### 问题 5：环境变量方式不生效

**可能原因**：环境变量设置有误

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

## 📌 下一步

配置验证成功后，让我们来做一个有趣的实践项目吧！

👉 **[实践：让 AI 帮你写个猜数字游戏 🎮](./first-project.md)**

如果遇到问题，查看 👉 **[常见问题解决](./troubleshooting.md)**
