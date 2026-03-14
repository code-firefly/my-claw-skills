# 推送失败解决方案

## 问题描述

在 WSL 环境中尝试推送到 GitHub 时遇到以下错误：

1. **TLS 连接错误**：
   ```
   GnuTLS recv error (-110): The TLS connection was non-properly terminated.
   ```

2. **SSH 权限错误**：
   ```
   ERROR: Permission to code-firefly/my-claw-skills.git denied to GreadXu.
   ```

## 问题分析

### TLS 错误原因

WSL 环境中的网络配置问题，导致 HTTPS 连接超时或失败。

### SSH 权限错误原因

- 当前 SSH 密钥属于 `GreadXu` 账户
- 仓库属于 `code-firefly` 账户
- `GreadXu` 没有该仓库的写权限

---

## 解决方案

### 方案 1：在 Windows 环境推送（推荐）

由于 WSL 网络问题，建议在 Windows 环境中推送：

#### 步骤 1：打开 Windows PowerShell

按 `Win + X`，选择 "Windows PowerShell"

#### 步骤 2：进入项目目录

```powershell
cd \\wsl$\Ubuntu\home\wangxg\projects\my-claw-skills
```

#### 步骤 3：查看 Git 状态

```powershell
git status
git log --oneline -5
```

#### 步骤 4：配置 GitHub 认证

**选项 A：GitHub CLI（推荐）**

```powershell
# 安装 GitHub CLI（如果未安装）
winget install --id GitHub.cli

# 登录 GitHub（选择 code-firefly 账户）
gh auth login

# 遵循提示完成认证
```

**选项 B：Personal Access Token**

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限：`repo`, `workflow`
4. 点击 "Generate token"
5. 复制 token

```powershell
# 配置 Git 使用 token
git config --global credential.helper store
git push -u origin main
# 输入用户名：code-firefly
# 输入密码：粘贴刚才复制的 token
```

#### 步骤 5：推送代码

```powershell
git push -u origin main
```

---

### 方案 2：添加 GreadXu 为协作者

如果你想让 GreadXu 账户也能推送，可以将其添加为协作者：

#### 步骤 1：在 GitHub 上添加协作者

1. 访问 https://github.com/code-firefly/my-claw-skills/settings/access
2. 点击 "Add people"
3. 输入：`GreadXu`
4. 选择权限：`Maintain`
5. 点击 "Add GreadXu"

#### 步骤 2：在 WSL 中使用 SSH 推送

```bash
cd /home/wangxg/projects/my-claw-skills

# 使用 SSH URL
git remote set-url origin git@github.com:code-firefly/my-claw-skills.git

# 推送（需要使用 GreadXu 的 SSH 密钥）
git push -u origin main
```

---

### 方案 3：使用 GitHub Desktop（最简单）

如果你安装了 GitHub Desktop：

#### 步骤 1：添加本地仓库

1. 打开 GitHub Desktop
2. File → Add Local Repository
3. 选择：`\\wsl$\Ubuntu\home\wangxg\projects\my-claw-skills`
4. 点击 "Add repository"

#### 步骤 2：推送到 GitHub

1. 点击 "Publish repository"
2. 输入仓库名：`my-claw-skills`
3. 确保 "Keep this code private" 未勾选
4. 点击 "Publish repository"

---

### 方案 4：修复 WSL 网络问题

如果你想继续在 WSL 中推送：

#### 选项 A：切换到 SSH（如果权限允许）

```bash
cd /home/wangxg/projects/my-claw-skills

# 切换到 SSH URL
git remote set-url origin git@github.com:code-firefly/my-claw-skills.git

# 测试连接
ssh -T git@github.com

# 推送
git push -u origin main
```

**注意**：这需要 `code-firefly` 账户的 SSH 密钥。

#### 选项 B：调整 Git 网络配置

```bash
cd /home/wangxg/projects/my-claw-skills

# 增加缓冲区大小
git config --global http.postBuffer 524288000

# 设置较低的安全级别（仅用于测试）
git config --global http.sslVerify false  # ⚠️ 不推荐用于生产

# 尝试推送
git push -u origin main
```

**注意**：禁用 SSL 验证有安全风险，仅用于测试。

#### 选项 C：配置代理

如果你的网络需要代理：

```bash
# 设置 HTTP 代理（替换为你的代理地址）
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080

# 推送
git push -u origin main

# 如果不需要代理，可以取消设置
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

## 推荐流程

### 最简单的流程

1. **打开 Windows PowerShell**
2. **进入项目目录**：`cd \\wsl$\Ubuntu\home\wangxg\projects\my-claw-skills`
3. **使用 GitHub CLI 登录**：`gh auth login`（选择 code-firefly 账户）
4. **推送代码**：`git push -u origin main`

### 如果成功

访问 https://github.com/code-firefly/my-claw-skills 确认代码已推送。

### 如果失败

记录错误信息，并提供：
- 完整的错误消息
- 使用的命令
- 操作系统版本
- Git 版本（`git --version`）

---

## 快速检查清单

在推送前，请确认：

- [ ] GitHub 仓库已创建：https://github.com/code-firefly/my-claw-skills
- [ ] 本地代码已提交（`git status` 显示 clean）
- [ ] 远程仓库已配置（`git remote -v`）
- [ ] Git 配置正确（用户名和邮箱）
- [ ] 网络连接正常
- [ ] 认证信息正确（GitHub CLI 或 token）

---

## 联系支持

如果以上方案都无法解决问题，请：

1. 检查 [GitHub Status](https://www.githubstatus.com/) 确保 GitHub 服务正常
2. 记录完整的错误信息
3. 提交 Issue：https://github.com/code-firefly/my-claw-skills/issues

---

*创建日期: 2026-03-13*
*最后更新: 2026-03-13*
