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

| 操作系统 | 支持版本 |
|---------|---------|
| **macOS** | macOS 11（Big Sur）及以上 |
| **Windows** | Windows 10 及以上 |

> ⚠️ **不支持** Windows 7 / 8 / 8.1。不满足要求的系统将**无法启动** CodeBuddy IDE。

### Step 1：下载安装包

| 版本 | 下载地址 |
|------|---------|
| 🇨🇳 国内版 | <https://www.codebuddy.cn/ide> |
| 🌍 国际版 | <https://www.codebuddy.ai/ide> |

打开上述链接，根据电脑的**处理器类型**（Apple Silicon / Intel / x64）选择对应版本下载。

**国内版下载页面：**

![国内版下载页面](./images/cn-download.png)

**国际版下载页面：**

![国际版下载页面](./images/intl-download.png)

### Step 2：安装

#### macOS

1. 下载完成后，**双击打开**安装包（`.dmg` 文件）
2. 在弹出的窗口中，将**左侧的 CodeBuddy 图标拖拽到右侧的 Applications 文件夹**中
3. 等待复制完成，安装即告完成

![macOS 安装 — 拖拽到 Applications](./images/intl-install-mac.png)

#### Windows

1. **双击**下载好的安装包（`.exe` 文件）
2. 若出现安装提示，选择 **「确定」**（表示仅为当前用户安装 CodeBuddy IDE）

![Windows 安装 — 安装提示](./images/cn-install-win-1.png)

3. 选择 **「我同意此协议」**，点击「下一步」

![Windows 安装 — 许可协议](./images/intl-install-win-license.png)

4. **选择安装位置**，点击「下一步」

![Windows 安装 — 选择安装位置](./images/intl-install-win-location.png)

5. 等待安装进度条完成，点击「完成」

![Windows 安装 — 安装完成](./images/intl-install-win-complete.png)

### Step 3：首次启动与导入设置

首次启动 CodeBuddy IDE，会自动检测并提示从以下编辑器导入设置：

- **VS Code**：扩展、快捷键、用户配置
- **Cursor**：扩展、快捷键、用户配置

> 💡 可以选择全部导入、部分导入或跳过，后续也可在设置中手动导入。

### Step 4：注册与登录

#### 国内版

打开 CodeBuddy IDE，点击 **「登录」** 按钮，浏览器会自动跳转到登录页面：

![国内版 IDE 登录按钮](./images/cn-login.png)

![国内版 Windows 登录按钮](./images/cn-login-win.png)

在浏览器登录页面选择登录方式：

![国内版登录页面](./images/cn-login-account.png)

| 登录方式 | 说明 |
|---------|------|
| **个人微信** | 使用微信扫码登录 |
| **手机号** | 输入手机号获取验证码登录 |

**企业用户**额外支持：

**SaaS 企业版（旗舰版）**：点击「登录」→ 选择「企业」中的「腾讯统一身份」

![SaaS 登录步骤](./images/cn-saas-login-1.png)
![SaaS 登录 — 腾讯统一身份](./images/cn-saas-login-2.png)

支持手机验证码 / 邮箱验证码 / SSO 登录：

![SaaS 登录 — 验证方式](./images/cn-saas-login-3.png)
![SaaS 登录 — 完成](./images/cn-saas-login-4.png)

**专有云企业版（专享版）**：联系企业管理员获取专享版，在浏览器登录页输入账号密码登录：

![专有云登录](./images/cn-private-login-1.png)
![专有云登录 — 输入账号](./images/cn-private-login-2.png)

> 💡 如果企业仅开通了企微认证源，将直接跳转企业微信扫码登录。

登录成功后，返回 IDE 即可开始使用：

![登录成功 — IDE](./images/cn-login-success-ide.png)

#### 国际版

**首次使用需先注册账号**：

1. 访问 [CodeBuddy 官网](https://www.codebuddy.ai/)，点击右上角 **「登录」**
2. 点击 **「注册」**，选择注册地区

![国际版 Web 登录/注册入口](./images/intl-web-login-signup.png)

3. 在注册页面选择注册方式：

![国际版注册页面](./images/intl-web-register.png)

| 注册 / 登录方式 | 说明 |
|----------------|------|
| **Google** | Google 账号授权登录 |
| **GitHub** | GitHub 账号授权登录 |
| **邮箱** | 邮箱注册并登录 |

![Google OAuth 登录](./images/intl-google-oauth.png)

注册成功后自动登录。之后打开 CodeBuddy IDE，点击 **「登录」** 按钮：

![国际版 macOS 登录按钮](./images/intl-login-mac.png)
![国际版 Windows 登录按钮](./images/intl-login-win.png)

浏览器跳转到账号登录页面，选择已有账号完成登录：

![国际版 Web 账号登录](./images/intl-web-account-login.png)
![macOS 选择账号](./images/intl-macos-select-account.png)

登录成功后，返回 CodeBuddy IDE 即可开始使用：

![macOS 登录成功](./images/intl-login-success-mac.png)

### Step 5：更新

1. 点击 IDE **右上方的「账户」图标**
2. 在菜单中选择 **「检查更新」**

![检查更新](./images/intl-check-update.png)

3. 如有新版本，左下方会显示推送通知，点击 **「立即安装」** 即可更新

### Step 6：设置与配置

进入设置页面后，左侧导航菜单包含以下模块：

![设置页面](./images/intl-settings.png)

| 模块 | 说明 |
|------|------|
| **通用** | 通用配置（主题、语言、字体等） |
| **对话** | 对话相关设置 |
| **Tab** | Tab 补全相关配置 |
| **文档** | 文档相关配置 |

> 📖 更多 IDE 安装与使用详情，请参考官方文档：
> - 国内版：<https://www.codebuddy.cn/docs/ide/Getting-Started/Installation>
> - 国际版：<https://www.codebuddy.ai/docs/zh/ide/Getting-Started/Installation>

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
