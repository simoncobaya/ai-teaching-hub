# CodeBuddy 安装指南

> CodeBuddy 提供三种产品形态，安装方式各不相同。

---

## 形态一览

| 形态 | 安装方式 | 适用场景 |
|------|---------|---------|
| **IDE（独立编辑器）** | 从官网下载安装包 | 想要开箱即用的 AI 编辑器体验 |
| **插件** | IDE 插件市场安装 | 已有 VS Code / JetBrains / 微信开发者工具工作流 |
| **CLI（CodeBuddy Code）** | npm 或 Homebrew 全局安装 | 终端操作、自动化脚本、CI/CD |

---

## 一、IDE（独立编辑器）

CodeBuddy IDE 是基于 Eclipse Theia 深度定制的**独立桌面应用程序**，不是 VS Code 插件。支持从 VS Code / Cursor 导入设置。

### 系统要求

| 要求 | 最低配置 | 推荐配置 |
|------|---------|---------|
| **操作系统** | Windows 10 / macOS 10.15 / Linux（Ubuntu 20.04+） | Windows 11 / macOS 12+ / Linux |
| **内存** | 8 GB | 16 GB |
| **存储空间** | 2 GB | 2 GB+ |

### 安装步骤

#### Step 1：下载安装包

| 版本 | 下载地址 |
|------|---------|
| 🇨🇳 国内版 | <https://www.codebuddy.cn/ide> |
| 🌍 国际版 | <https://www.codebuddy.ai/ide> |

打开上述链接，选择对应操作系统的安装包进行下载。

#### Step 2：安装

| 系统 | 操作 |
|------|------|
| **macOS** | 打开 `.dmg` 文件，将 CodeBuddy 拖入 Applications 文件夹 |
| **Windows** | 运行 `.exe` 安装程序，按提示完成安装 |
| **Linux** | 使用 `.AppImage` 或对应发行版包格式安装 |

#### Step 3：导入已有设置（可选）

首次启动后，IDE 支持从 VS Code / Cursor 导入扩展、快捷键和用户设置。

#### Step 4：登录

使用对应版本的账号登录：

- **国内版**：微信扫码等国内账号体系
- **国际版**：Google / GitHub 等国际账号体系

---

## 二、插件

插件版本安装到已有的 VS Code / JetBrains / 微信开发者工具中使用。

### VS Code

1. 打开 VS Code
2. 进入扩展面板（`Ctrl + Shift + X` / `Cmd + Shift + X`）
3. 搜索 **"CodeBuddy"**
4. 点击安装

### JetBrains 系（IntelliJ IDEA / PyCharm / WebStorm 等）

1. 打开 IDE → Settings → Plugins
2. 在 Marketplace 中搜索 **"CodeBuddy"**
3. 点击 Install，重启 IDE

### 微信开发者工具

在微信开发者工具的扩展市场中搜索 **"CodeBuddy"** 安装。

> ⚠️ 插件支持 **Ask 和 Craft** 模式，不支持 Plan 模式（Plan 仅限 IDE 和 CLI）。

---

## 三、CLI（CodeBuddy Code）

CodeBuddy Code 是 CodeBuddy 的命令行工具，于 2025 年 9 月 9 日发布。

### 前置要求

- Node.js **18.0** 及以上版本

### 安装方式

#### 方式一：npm（推荐）

```bash
npm install -g @tencent-ai/codebuddy-code
```

#### 方式二：Homebrew（macOS / Linux）

```bash
brew install Tencent-CodeBuddy/tap/codebuddy-code
```

### 验证安装

```bash
codebuddy --version
```

### 登录

首次使用需要登录，在终端运行 `codebuddy` 后会显示站点选择界面：

| 登录选项 | 对应地址 | 认证方式 |
|---------|---------|---------|
| **Chinese Site** | copilot.tencent.com | 微信扫码 |
| **International Site** | codebuddy.ai | Google / GitHub |
| **Enterprise Domain** | 企业专属域名 | 企业账号 |
| **iOA** | 腾讯内部 | iOA 认证 |

> CLI 是**同一个工具**，安装后通过登录站点区分国内版 / 国际版，无需安装不同的包。

### 常用命令

| 命令 | 说明 |
|------|------|
| `codebuddy` | 启动交互式会话 |
| `codebuddy --version` | 查看版本 |
| `codebuddy --help` | 查看帮助 |

---

## 安装后验证

| 形态 | 验证方法 |
|------|---------|
| **IDE** | 启动 CodeBuddy，打开项目，按 `⌘ + I`（macOS）/ `Ctrl + I`（Windows）唤起内联对话 |
| **插件** | 在编辑器中查看 CodeBuddy 状态栏图标是否亮起 |
| **CLI** | 在终端运行 `codebuddy --version` 确认输出版本号 |

---

## 常见问题

### Q：IDE 和插件应该装哪个？

| 场景 | 推荐 |
|------|------|
| 想要开箱即用，需要 Figma 转代码 / 后端集成 / 一键部署 | IDE |
| 已有成熟的 VS Code / JetBrains 工作流 | 插件 |
| 两者都装 | 完全可以，它们是独立的产品 |

### Q：国内版和国际版的 CLI 需要分别安装吗？

不需要。CLI 是同一个 npm 包，安装后在登录时选择站点即可。

### Q：CLI 支持哪些操作系统？

macOS、Windows、Linux 均可使用，前提是已安装 Node.js 18.0+。
