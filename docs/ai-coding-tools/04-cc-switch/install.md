# 📥 安装 CC Switch

> CC Switch 安装超简单，就像安装普通软件一样！

---

## 🎯 目标

在你的电脑上安装 CC Switch 桌面应用。

---

> 💡 **版本说明**：本教程以 CC Switch v3.16.1 为例，但建议安装 **最新版本**（GitHub Releases 页面会自动显示最新版）。安装步骤基本相同，直接用最新版就好！

---

## 🚀 安装步骤

### Windows 系统

#### 方式一：安装包（推荐）

1. 下载安装包（任选一种）：
   - 📦 **指定版本下载**：[CC-Switch-v3.16.1-Windows.msi](https://github.com/farion1231/cc-switch/releases/download/v3.16.1/CC-Switch-v3.16.1-Windows.msi)
   - 🌐 **GitHub 下载**：在 https://github.com/farion1231/cc-switch/releases 找到并下载 **`CC-Switch-vX.X.X-Windows.msi`**
2. 双击下载的 `.msi` 文件
3. 按照安装向导操作，一路"下一步"
4. 安装完成！在桌面或开始菜单找到 CC Switch 打开

#### 方式二：便携版（免安装）

1. 下载便携版（任选一种）：
   - 📦 **指定版本下载**：[CC-Switch-v3.16.1-Windows-Portable.zip](https://github.com/farion1231/cc-switch/releases/download/v3.16.1/CC-Switch-v3.16.1-Windows-Portable.zip)
   - 🌐 **GitHub 下载**：在 https://github.com/farion1231/cc-switch/releases 找到并下载 **`CC-Switch-vX.X.X-Windows-Portable.zip`**
2. 解压到任意文件夹
3. 双击 `CC-Switch.exe` 运行

> 💡 便携版适合不想安装或没有管理员权限的情况。

---

### macOS 系统

#### 方式一：Homebrew（推荐）

如果你已经安装了 Homebrew：

```bash
# 添加 CC Switch 的源
brew tap farion1231/ccswitch

# 安装 CC Switch
brew install --cask cc-switch
```

更新到最新版：

```bash
brew upgrade --cask cc-switch
```

#### 方式二：手动下载

1. 下载安装包（任选一种）：
   - 📦 **指定版本下载**：[CC-Switch-v3.16.1-macOS.dmg](https://github.com/farion1231/cc-switch/releases/download/v3.16.1/CC-Switch-v3.16.1-macOS.dmg)
   - 🌐 **GitHub 下载**：在 https://github.com/farion1231/cc-switch/releases 找到并下载 **`CC-Switch-vX.X.X-macOS.dmg`**
2. 双击 `.dmg` 文件
3. 把 CC Switch 拖到"Applications"文件夹
4. 在启动台（Launchpad）找到 CC Switch 打开

> ⚠️ 首次打开时，macOS 可能提示"无法验证开发者"。右键点击应用 → 选择"打开" → 点击"打开"确认即可。

---

### Linux 系统

1. 下载对应你的发行版的安装包（任选一种）：

   **指定版本下载**：
   - **Ubuntu/Debian**：[CC-Switch-v3.16.1-Linux-x86_64.deb](https://github.com/farion1231/cc-switch/releases/download/v3.16.1/CC-Switch-v3.16.1-Linux-x86_64.deb)
   - **Fedora/RHEL**：[CC-Switch-v3.16.1-Linux-x86_64.rpm](https://github.com/farion1231/cc-switch/releases/download/v3.16.1/CC-Switch-v3.16.1-Linux-x86_64.rpm)
   - **通用**（免安装）：[CC-Switch-v3.16.1-Linux-x86_64.AppImage](https://github.com/farion1231/cc-switch/releases/download/v3.16.1/CC-Switch-v3.16.1-Linux-x86_64.AppImage)

   **GitHub 下载**：在 https://github.com/farion1231/cc-switch/releases 找到并下载对应文件（`.deb` / `.rpm` / `.AppImage`）
2. 安装：
   ```bash
   # Ubuntu/Debian
   sudo dpkg -i CC-Switch-vX.X.X-Linux.deb

   # Fedora/RHEL
   sudo rpm -i CC-Switch-vX.X.X-Linux.rpm

   # AppImage（免安装）
   chmod +x CC-Switch-vX.X.X-Linux.AppImage
   ./CC-Switch-vX.X.X-Linux.AppImage
   ```

---

## 🎉 启动 CC Switch

安装完成后，启动 CC Switch：

- **Windows**：开始菜单 → CC Switch
- **macOS**：启动台 → CC Switch
- **Linux**：应用菜单 → CC Switch

第一次启动时，你会看到 CC Switch 的主界面，列出了所有支持的 AI 工具。

---

## ✅ 验证安装

CC Switch 启动后，检查：

1. ✅ 能看到工具列表（Claude Code、Codex、OpenCode 等）
2. ✅ 能看到供应商管理页面
3. ✅ 没有报错信息

---

## ❓ 常见问题

### Q：Windows 安装时提示"已被 SmartScreen 阻止"？

点击 **"更多信息"** → **"仍要运行"**。这是因为 CC Switch 是开源软件，没有购买微软的数字证书。

### Q：macOS 提示"无法打开，因为它来自身份不明的开发者"？

右键点击应用 → 选择 **"打开"** → 在弹出的对话框中点击 **"打开"**。

### Q：下载速度很慢？

GitHub 在国内可能下载慢。可以试试：
- 📦 使用上面的 **指定版本下载** 链接（直接下载，不用在 Releases 页面里找文件）
- 使用 GitHub 镜像站
- 让老师或同学帮忙下载
- 使用网络加速工具

> ⚠️ 以上"指定版本下载"链接指向 CC Switch v3.16.1，这是一个固定版本，可能会随着时间过期失效。如果无法下载，请使用 GitHub Releases 页面获取最新版本。

---

## 📌 下一步

CC Switch 安装好了！接下来添加你的第一个 API 供应商。

👉 **[添加 API 供应商](./add-provider.md)** — 添加 DeepSeek
