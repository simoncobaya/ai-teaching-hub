# 🟢 安装 Node.js

> Claude Code 需要 Node.js 才能运行。就像手机需要安卓或 iOS 系统才能运行 App，Claude Code 需要 Node.js 才能运行。

---

## 🤔 Node.js 是什么？

**Node.js** 是一个让 JavaScript 在电脑上运行的工具。Claude Code 就是用 Node.js 开发的，所以需要先安装它。

你不需要学会 Node.js 编程！只需要安装好就行，就像安装一个普通软件一样 👇

---

## 🔍 先检查：你的电脑上有没有 Node.js？

在安装之前，先确认一下你的电脑上是不是已经有 Node.js 了！（有些电脑可能预装了）

1. 打开终端：
   - **Windows**：按 `Win + R`，输入 `cmd`，回车
   - **macOS**：按 `Command + 空格`，搜索 `Terminal`，打开
   - **Linux**：按 `Ctrl + Alt + T`

2. 输入下面的命令，然后按回车：

```bash
node --version
```

3. 看看显示了什么：

| 你看到的 | 意思 | 怎么做 |
|---------|------|--------|
| `v24.x.x` 或 `v22.x.x` 等（版本号 ≥ v18） | ✅ **已经安装了！** | 🎉 跳过这页，直接看下一页！ |
| `v16.x.x` 或更低（版本号 < v18） | ⚠️ 版本太旧了 | 继续往下看，安装新版本 |
| `'node' 不是内部或外部命令` | ❌ 没安装 Node.js | 继续往下看，开始安装 |

> 💡 如果你看到版本号 ≥ v18，那你已经装好了，不需要再装一遍！直接跳到下一页 👉 [安装 Claude Code](./03-claude-code.md)

---

## 🚀 安装步骤

### Windows 系统

#### 方式一：下载安装（⭐ 推荐）

1. 下载安装包（任选一种）：
   - 📦 **指定版本下载**：[node-v24.16.0-x64.msi](https://nodejs.org/dist/v24.16.0/node-v24.16.0-x64.msi)
   - 🌐 **官网下载**：https://nodejs.org/ 下载 **LTS 版本**
2. 双击下载的 `.msi` 文件
3. 一路点击 **"Next"（下一步）**
4. 安装完成！🎉

> ⚠️ 以上"指定版本下载"链接指向 Node.js v24.16.0，这是一个固定版本，可能会随着时间过期失效。如果无法下载，请使用下方的官网下载方式获取最新版本。

> 💡 安装时确保勾选了 **"Add to PATH"**（一般默认已勾选）。
>
> 💡 **版本说明**：本教程以 Node.js v24.16.0 为例，但建议安装 **最新 LTS 版本**（官网 https://nodejs.org/ 会自动显示最新版）。安装步骤基本相同，直接用最新版就好！

#### 方式二：使用 winget（Windows 10/11 自带）

打开 PowerShell 或 CMD，输入：

```powershell
winget install OpenJS.NodeJS.LTS
```

---

### macOS 系统

#### 方式一：下载安装（⭐ 推荐）

1. 下载安装包（任选一种）：
   - 📦 **指定版本下载**：[node-v24.16.0.pkg](https://nodejs.org/dist/v24.16.0/node-v24.16.0.pkg)
   - 🌐 **官网下载**：https://nodejs.org/ 下载 **LTS 版本**
2. 双击 `.pkg` 安装包
3. 一路点击 **"Continue"（继续）**
4. 安装完成！🎉

> ⚠️ 以上"指定版本下载"链接指向 Node.js v24.16.0，这是一个固定版本，可能会随着时间过期失效。如果无法下载，请使用下方的官网下载方式获取最新版本。

#### 方式二：使用 Homebrew（适合已安装 Homebrew 的同学）

```bash
brew install node@24
```

> 💡 如果没有安装 Homebrew，推荐用方式一。

---

### Linux 系统

#### 方式一：下载安装（⭐ 推荐）

下载 Linux 版 Node.js 安装包：

- 📦 **指定版本下载**：[node-v24.16.0-linux-x64.tar.xz](https://nodejs.org/dist/v24.16.0/node-v24.16.0-linux-x64.tar.xz)

> ⚠️ 以上"指定版本下载"链接指向 Node.js v24.16.0，这是一个固定版本，可能会随着时间过期失效。如果无法下载，请使用下方的在线安装方式。

```bash
# 1. 解压安装包
tar -xJf node-v24.16.0-linux-x64.tar.xz

# 2. 移动到系统目录
sudo mv node-v24.16.0-linux-x64 /usr/local/node

# 3. 添加到 PATH 环境变量
echo 'export PATH="/usr/local/node/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### 方式二：在线安装

**Ubuntu / Debian：**

```bash
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Fedora / RHEL：**

```bash
curl -fsSL https://rpm.nodesource.com/setup_24.x | sudo bash -
sudo dnf install -y nodejs
```

#### 方式三：使用 nvm（适合多版本管理）

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# 重新打开终端，然后安装最新 LTS 版本
nvm install --lts
```

> 💡 nvm 可以让你在不同版本的 Node.js 之间切换，非常方便！

---

## ✅ 验证安装

安装完成后，打开**新的**终端窗口（重要！），输入：

```bash
node --version
```

如果显示版本号（如 `v24.x.x`），说明安装成功！🎉

再验证一下 npm（Node.js 自带的包管理器）：

```bash
npm --version
```

如果也显示版本号，说明一切就绪！

---

## ❓ 常见问题

### Q："'node' 不是内部或外部命令"

**可能原因**：Node.js 没有正确安装，或者安装后没有重新打开终端。

**解决方法**：
1. **关闭终端，重新打开** 再试
2. 如果还不行，重启电脑
3. 如果还是不行，重新安装 Node.js，确保勾选了 "Add to PATH"

### Q：版本太旧怎么办？

有些工具需要 **Node.js 18 或更高版本**。检查版本：

```bash
node --version
```

如果版本低于 v18：
- **Windows / macOS**：用上面的方式一重新安装
- **Linux**：使用 nvm 方式安装最新版

### Q：官网下载很慢？

Node.js 官网在国内可能下载较慢。可以试试：
- 📦 使用上面的 **指定版本下载** 链接
- 🇨🇳 **国内镜像**：https://npmmirror.com/mirrors/node/
- 让老师或同学帮忙用 U 盘拷贝安装包

---

[⬅️ 上一页：认识 DeepSeek](./01-deepseek.md) | [➡️ 下一页：认识 + 安装 Claude Code](./03-claude-code.md)
