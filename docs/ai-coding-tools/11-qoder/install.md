# 📥 下载安装 Qoder

---

## Qoder IDE 安装

前往官网下载对应平台的安装包：

| 版本 | 下载地址 |
|------|---------|
| 🇨🇳 国内版 | https://qoder.com.cn/ |
| 🌍 国际版 | https://qoder.com |

### Windows

1. 下载 Windows 安装包
2. 双击运行安装程序
3. 按照向导完成安装
4. 启动 Qoder

### macOS

1. 下载 macOS 安装包（.dmg）
2. 双击打开
3. 拖动到 Applications 文件夹
4. 在启动台打开 Qoder

### Linux

1. 下载对应发行版的安装包
2. 安装：
   ```bash
   # Ubuntu/Debian
   sudo dpkg -i qoder_xxx.deb

   # Fedora/RHEL
   sudo rpm -i qoder_xxx.rpm
   ```

---

## Qoder CLI 安装

> ⚠️ 国内版和国际版 CLI 的 **包名不同**，请注意区分！

### 🇨🇳 国内版（Qoder CN CLI）

支持 macOS、Linux、Windows（Windows Terminal）

#### macOS / Linux

```bash
curl -fsSL https://qoder.com.cn/install | bash
```

#### Windows PowerShell

```powershell
irm https://qoder.com.cn/install.ps1 | iex
```

#### Windows CMD

```cmd
curl -fsSL https://qoder.com.cn/install.cmd -o install.cmd && install.cmd
```

#### npm（macOS / Linux / Windows 通用）

```bash
npm install -g @qodercn-ai/qoderclicn
```

> 💡 国内镜像加速：`npm install -g @qodercn-ai/qoderclicn --registry=https://registry.npmmirror.com`

#### 验证安装

```bash
qoderclicn --version
```

#### 登录

```bash
# 启动 CLI
qoderclicn

# 在交互式提示符中登录
/login
```

登录方式：
- **login with browser**：打开浏览器登录（推荐）
- **login with qodercn personal access token**：粘贴 Token 登录

> 获取 Personal Access Token：https://qoder.com.cn/account/integrations

#### 环境变量登录（CI/CD）

```bash
# macOS / Linux
export QODERCN_PERSONAL_ACCESS_TOKEN="your_token"

# Windows CMD
set QODERCN_PERSONAL_ACCESS_TOKEN="your_token"

# Windows PowerShell
$env:QODERCN_PERSONAL_ACCESS_TOKEN = "your_token"
```

> 📖 国内版完整文档：https://help.aliyun.com/zh/lingma/qodercli-cn/user-guide/qoder-cli-cn-get-started-quickly

---

### 🌍 国际版（Qoder CLI）

#### macOS / Linux

```bash
curl -fsSL https://qoder.com/install | bash
```

#### Windows PowerShell

```powershell
irm https://qoder.com/install.ps1 | iex
```

#### Windows CMD

```cmd
curl -fsSL https://qoder.com/install.cmd -o install.cmd && install.cmd
```

#### npm（macOS / Linux / Windows 通用）

```bash
npm install -g @qoder-ai/qodercli
```

#### 验证安装

```bash
qodercli --version
```

> 📖 国际版完整文档：https://docs.qoder.com/en/cli/quick-start

---

## IDE 插件安装

Qoder 也提供 IDE 插件：

1. 打开你的 IDE（VS Code / JetBrains）
2. 在插件市场搜索 **"Qoder"**
3. 点击安装
4. 重启 IDE

---

## 📌 下一步

👉 **[国内版 vs 国际版](./versions.md)**
