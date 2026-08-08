# CodeBuddy 国内版 vs 国际版

> CodeBuddy 有两个独立的官网和账号体系，分别面向中国大陆和全球开发者。

---

## 核心结论

| 问题 | 答案 |
|------|------|
| 是同一个工具吗？ | **CLI 是同一工具**（登录时选站点）；**IDE 需从各自官网下载** |
| 账号互通吗？ | **不互通**，各自独立的账号体系 |
| CLI 如何区分版本？ | 安装后登录时选择站点（Chinese Site / International Site） |
| IDE 如何区分版本？ | 从对应官网下载不同安装包 |

---

## 版本对比

| 维度 | 国内版 | 国际版 |
|------|--------|--------|
| **官网** | https://www.codebuddy.cn/ | https://www.codebuddy.ai/ |
| **文档** | https://www.codebuddy.cn/docs | https://www.codebuddy.ai/docs |
| **CLI 登录地址** | copilot.tencent.com（微信扫码） | codebuddy.ai（Google / GitHub） |
| **账号体系** | 微信等国内账号 | Google / GitHub 等国际账号 |
| **IDE 下载** | https://www.codebuddy.cn/ide | https://www.codebuddy.ai/ide |

---

## CLI：同一工具，登录时选择站点

CodeBuddy CLI（CodeBuddy Code）是**同一个 npm 包**，安装后在首次使用时选择登录站点：

| 登录选项 | 对应地址 | 认证方式 |
|---------|---------|---------|
| **Chinese Site** | copilot.tencent.com | 微信扫码 |
| **International Site** | codebuddy.ai | Google / GitHub |
| **Enterprise Domain** | 企业专属域名 | 企业账号 |
| **iOA** | 腾讯内部 | iOA 认证 |

---

## IDE：各自独立下载

CodeBuddy IDE 需从对应官网下载安装包：

- 🇨🇳 国内版 IDE：<https://www.codebuddy.cn/ide>
- 🌍 国际版 IDE：<https://www.codebuddy.ai/ide>

> 2025 年 8 月 21 日，CodeBuddy IDE **国内版**正式开放公测。

---

## 如何选择？

| 你的情况 | 推荐版本 |
|---------|---------|
| 在中国大陆，使用国内云服务 | 🇨🇳 国内版 |
| 面向海外市场，使用国际云服务 | 🌍 国际版 |
| 团队在国内，需要合规和本地化支持 | 🇨🇳 国内版 |
| 全球化团队，跨地区协作 | 🌍 国际版 |

---

## 常见误区

### ❌ 误区 1：IDE 是 VS Code 插件

CodeBuddy IDE 是基于 Eclipse Theia 深度定制的**独立桌面编辑器**，类似于 Cursor。它与插件版本是完全不同的产品形态。插件版本安装到 VS Code / JetBrains / 微信开发者工具中作为扩展使用，而 IDE 版本是独立运行的应用程序。

### ❌ 误区 2：`--region` 参数切换版本

CodeBuddy CLI 不存在 `codebuddy login --region cn` 这样的命令。CLI 是同一工具，安装后在交互式登录流程中选择站点即可。

### ❌ 误区 3：所有形态都有独立的"国内版"和"国际版"

- **CLI**：同一 npm 包，登录时选站点
- **IDE**：从各自官网下载不同安装包
- **插件**：在 IDE 插件市场搜索安装，登录时区分账号
