# 📥 安装 OpenCode

---

## 🚀 安装步骤

### Windows 系统

#### 方式一：npm（推荐）

打开 PowerShell 或 CMD，输入：

```bash
npm install -g opencode
```

> 💡 需要先安装 Node.js（👉 [安装 Node.js 教程](../00-introduction/install-nodejs.md)）

#### 方式二：Go

先安装 Go（👉 [Go 官网](https://go.dev/dl/)），然后：

```bash
go install github.com/anomalyco/opencode@latest
```

---

### macOS 系统

#### 方式一：安装脚本（推荐）

```bash
curl -fsSL https://opencode.ai/install.sh | sh
```

#### 方式二：Homebrew

```bash
brew install opencode
```

#### 方式三：npm

```bash
npm install -g opencode
```

#### 方式四：Go

```bash
go install github.com/anomalyco/opencode@latest
```

---

### Linux 系统

#### 方式一：安装脚本（推荐）

```bash
curl -fsSL https://opencode.ai/install.sh | sh
```

#### 方式二：npm

```bash
npm install -g opencode
```

#### 方式三：Homebrew

```bash
brew install opencode
```

#### 方式四：Go

```bash
go install github.com/anomalyco/opencode@latest
```

---

## 验证安装

```bash
opencode --version
```

显示版本号即安装成功！🎉

---

## 启动

在项目目录中：

```bash
opencode
```

---

## ❓ 常见问题

### Q：npm 安装在 Windows 上有问题？

试试用安装脚本或 Go 方式安装。

### Q：安装后找不到命令？

关闭终端重新打开，或重启电脑。

---

## 📌 下一步

👉 **[基础用法](./basics.md)**

👉 **[配置各种模型](./configure-models.md)**
