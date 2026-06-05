# 🔌 添加 API 供应商

> 把你的 DeepSeek API Key 添加到 CC Switch，让它帮你配置所有工具！

---

## 🎯 目标

在 CC Switch 中添加 DeepSeek 供应商，并配置好 API Key。

---

> 💡 **界面提示**：CC Switch 偶尔会更新界面，截图可能与实际页面略有不同，但整体流程是相似的。如果找不到某个按钮，试着找找类似位置的相同文字哦！

---

## 🚀 操作步骤

### Step 1：打开供应商管理

1. 启动 CC Switch
2. 在主界面，点击右上角的 **橙色「+」按钮** 添加供应商

![CC Switch 添加供应商入口](./images/ccswitch-add-provider-entry.png)

> 💡 主界面会显示已添加的供应商卡片（比如默认的 Claude Official）。

---

### Step 2：选择 DeepSeek 并填写基础配置

CC Switch 内置了 **50+ API 供应商预设**，你不需要手动填写大部分配置：

1. 在弹出的添加供应商窗口中，先点击顶部的 **「Claude 供应商」** 按钮
2. 在预设列表中找到 **「DeepSeek」**，点击选择它
3. 在 **「API Key」** 输入框中，粘贴你的 DeepSeek API Key

![基础配置：选择 DeepSeek 并填入 API Key](./images/ccswitch-provider-basic-config.png)

你的 API Key 看起来像这样：`sk-xxxxxxxxxxxxxxxx`

> ⚠️ API Key 是你的密码，不要给别人看！

其他配置项 CC Switch 已经帮你自动填好了：

| 配置项 | 自动填写的内容 |
|--------|--------------|
| 供应商名称 | DeepSeek |
| 请求地址 | `https://api.deepseek.com/anthropic` |

---

### Step 3：配置高级选项并保存

基础信息填好后，**下滑页面**，展开「高级选项」区域：

![高级选项：模型映射、1M 上下文、最大强度思考](./images/ccswitch-provider-advanced-config.png)

检查并确认以下设置：

1. **模型映射**：确认勾选了 **「1M」** 上下文（这样 Claude Code 可以处理更长的代码）
2. **最大强度思考**：确认 **已勾选**（让 AI 思考更深入）
3. **兜底模型**：确认显示 `deepseek-v4-pro[1m]`

> ⚠️ 以上这些不是默认设置，**需要你手动勾选和填写**，别忘了！

确认无误后，点击右下角的 **「添加」** 按钮保存配置。

---

### Step 4：测试连接

保存成功后，回到主界面。现在来测试一下 DeepSeek 能不能正常连接：

1. 找到 **DeepSeek** 卡片
2. 点击卡片上的 **编辑图标（铅笔）** 测试模型

![测试模型连接](./images/ccswitch-test-success.png)

如果看到 **「DeepSeek 运行正常 ✅」** 和响应时间，说明配置成功了！🎉

> 💡 如果测试失败，请检查 API Key 是否正确，或者网络是否能访问 DeepSeek。

---

### Step 5：配置用量查询（推荐）

配置用量查询后，CC Switch 会自动显示你的 DeepSeek 账户余额，方便你随时查看。

1. 找到 DeepSeek 卡片，点击 **图表图标（📊）** 进入用量查询配置

![用量查询入口](./images/ccswitch-usage-query-entry.png)

2. 在配置页面中：
   - 打开 **「启用用量查询」** 开关
   - 选择 **「官方」** 模板标签页
   - 点击 **「保存配置」**

![用量查询配置](./images/ccswitch-usage-query-config.png)

> 💡 选择「官方」模板后，CC Switch 会自动用你的 API Key 查询余额，不需要额外配置！

---

### Step 6：启用 DeepSeek

回到主界面，找到 DeepSeek 卡片，点击 **「启用」** 按钮：

![启用 DeepSeek](./images/ccswitch-enable-deepseek.png)

---

### Step 7：验证成功 ✅

启用后，确认 DeepSeek 卡片上显示：

- ✅ **「使用中」** 状态 — 说明 Claude Code 现在使用的是 DeepSeek
- ✅ **余额信息** — 显示你账户的剩余金额（如：剩余 49.99 CNY）

![DeepSeek 已启用并使用中](./images/ccswitch-deepseek-active.png)

看到这些信息，说明你已经配置成功了！🎉🎉🎉

---

## 🎉 完成！

你已经成功添加了 DeepSeek 供应商！现在 CC Switch 可以帮你：
- 把 DeepSeek 配置应用到 Claude Code
- 一键切换到 DeepSeek 模型
- 随时查看账户余额

---

## 📦 添加更多供应商（可选）

CC Switch 支持 50+ 供应商预设（智谱 GLM、Anthropic Claude、OpenAI 等）。如果你有其他 AI 的 API Key，用同样的方式点击橙色「+」按钮添加即可。

---

## ❓ 常见问题

### Q：预设列表里没有我想要的供应商？

选择 **「自定义」**，然后手动填写：
- 供应商名称
- 请求地址（Base URL）
- API Key
- 模型名称

### Q：添加了多个供应商，怎么选？

你可以在供应商列表中点击某个供应商的 **「启用」** 按钮，让它成为当前使用的供应商。

### Q：测试连接失败怎么办？

检查以下几点：
- API Key 是否正确（以 `sk-` 开头）
- 网络能否访问 DeepSeek（`https://api.deepseek.com`）
- DeepSeek 账户是否有余额

---

## 📌 下一步

供应商添加好了！接下来学习怎么切换模型。

👉 **[一键切换模型](./switch-model.md)** — 在不同模型之间快速切换
