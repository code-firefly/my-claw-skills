# GitHub 仓库设置指南

本文档提供完整的 GitHub 仓库设置和推送步骤。

---

## 📋 前置准备

### 1. 确认 Git 配置

```bash
git config --global user.name "code-firefly"
git config --global user.email "your-email@example.com"
```

### 2. 检查当前状态

```bash
cd /home/wangxg/projects/my-claw-skills
git status
git log --oneline -5
```

---

## 🚀 创建 GitHub 仓库

### 方式 1：GitHub Web UI（推荐）

1. 打开 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `my-claw-skills`
   - **Description**: `OpenClaw 技能集合 - 完整的学习管理系统`
   - **Public/Private**: Public（推荐，因为是开源技能）
   - **Initialize this repository**: ❌ 不要勾选（我们已有本地仓库）
3. 点击 "Create repository"
4. 复制仓库 URL：`https://github.com/code-firefly/my-claw-skills.git`

### 方式 2：GitHub CLI

```bash
# 如果没有安装 gh CLI
# Ubuntu/Debian: sudo apt install gh
# macOS: brew install gh

# 登录
gh auth login

# 创建仓库
gh repo create my-claw-skills --public --description "OpenClaw 技能集合" --source=. --remote=origin --push
```

---

## 📤 推送代码到 GitHub

### Step 1：添加远程仓库

```bash
cd /home/wangxg/projects/my-claw-skills
git remote add origin https://github.com/code-firefly/my-claw-skills.git
```

### Step 2：重命名默认分支（推荐）

```bash
git branch -M main
```

### Step 3：推送到 GitHub

```bash
git push -u origin main
```

### Step 4：验证

在浏览器中打开：https://github.com/code-firefly/my-claw-skills

---

## ⚙️ 配置 GitHub 仓库

### 1. 设置仓库描述

在仓库页面：
- 点击 "Settings" → "General"
- 在 "Description" 中填写：
  ```
  OpenClaw 技能集合 - 完整的学习管理系统，支持学习目标管理、课程学习、进度追踪、书签管理和知识缓存
  ```
- 点击 "Save changes"

### 2. 添加 Topics

在 "Topics" 中添加以下标签：
```
openclaw, skills, learning, education, progress-tracking, bookmarks, knowledge-management, chinese
```

### 3. 设置默认分支

在 "Settings" → "Branches"：
- 设置 "main" 为默认分支

### 4. 启用 GitHub Pages（可选）

如果你想托管技能文档：
- 点击 "Settings" → "Pages"
- 在 "Source" 中选择：
  - Branch: `main`
  - Folder: `/docs` 或 `/root`
- 点击 "Save"

### 5. 配置 GitHub Secrets（用于 ClawHub 自动发布）

在 "Settings" → "Secrets and variables" → "Actions" → "New repository secret":
- Name: `CLAWHUB_TOKEN`
- Value: 你的 ClawHub API Token

获取 ClawHub Token：
```bash
clawhub login
# Token 会保存在 ~/.clawhub/config.json
```

---

## 🔄 后续更新流程

### 日常开发

```bash
cd /home/wangxg/projects/my-claw-skills

# 1. 修改文件
# ... 编辑文件 ...

# 2. 提交更改
git add .
git commit -m "feat: 添加新功能"

# 3. 推送到 GitHub
git push origin main
```

### 发布新版本

```bash
cd /home/wangxg/projects/my-claw-skills

# 1. 更新版本号
echo "1.0.1" > VERSION

# 2. 更新 CHANGELOG.md
# ... 编辑 CHANGELOG.md ...

# 3. 更新 metadata.json 中的版本号
# ... 编辑 metadata.json ...

# 4. 提交更改
git add .
git commit -m "chore: release v1.0.1"

# 5. 创建 tag
git tag v1.0.1

# 6. 推送 tag
git push origin main
git push origin v1.0.1
```

### GitHub Actions 自动发布

推送 tag 后，GitHub Actions 会自动：
1. 检出代码
2. 安装 ClawHub CLI
3. 发布到 ClawHub
4. 创建 GitHub Release

---

## 🔗 关联 my-skills 仓库

在 `my-skills` 仓库中：

### 1. 更新 PLATFORM_MATRIX.md

```markdown
### OpenClaw Platform Details

| Skill | Status | Repository | OpenClaw Ver | Converted | Tested |
|-------|--------|------------|--------------|-----------|--------|
| learn-system-openclaw | ✅ 1.0.0 | code-firefly/my-claw-skills | 1.0.0 | 2026-03-13 | 待测试 |

**说明**：
- learn-system-openclaw 已迁移到独立仓库：https://github.com/code-firefly/my-claw-skills
- 完全独立维护，不再与 my-skills 同步
- ClawHub 发布：learn-system-openclaw（待发布）
```

### 2. 更新 AGENTS.md

```markdown
## 专项技能仓库

### OpenClaw 技能集合

- **仓库**: https://github.com/code-firefly/my-claw-skills
- **描述**: OpenClaw 专项技能集合
- **当前技能**:
  - learn-system-openclaw (学习管理系统)
- **维护方式**: 完全独立，不再与 my-skills 同步
```

### 3. 提交更新

```bash
cd /home/wangxg/projects/my-skills
git add .
git commit -m "docs: learn-system-openclaw 迁移到独立仓库"
git push origin main
```

---

## ✅ 验证清单

推送完成后，请验证：

- [ ] 仓库页面可以正常访问
- [ ] README.md 显示正常
- [ ] LICENSE 显示正常
- [ ] 所有文件都已推送
- [ ] GitHub Actions 工作流已启用
- [ ] 仓库描述和 Topics 已设置
- [ ] 默认分支为 `main`
- [ ] (可选) GitHub Pages 已配置

---

## 📞 获取帮助

遇到问题？

1. 检查 [GitHub 文档](https://docs.github.com/)
2. 查看 [ClawHub 文档](https://clawhub.com/docs)
3. 提交 Issue: https://github.com/code-firefly/my-claw-skills/issues

---

## 🎉 完成！

现在你的 `my-claw-skills` 仓库已经设置完成，可以：
- 继续开发新技能
- 发布到 ClawHub
- 接受社区贡献

祝开发愉快！🚀

---

*创建日期: 2026-03-13*
*最后更新: 2026-03-13*
