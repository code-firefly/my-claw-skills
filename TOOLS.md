# TOOLS.md - Skill Developer Tools

## ClawHub CLI

ClawHub 是 OpenClaw 技能分发平台，用于搜索、安装、发布和管理技能。

### 配置
- **配置文件**: `~/.clawhub/config.json`
- **Registry**: https://clawhub.com
- **当前 Token**: 已配置（code-firefly 账户）

### 常用命令

#### 搜索技能
```bash
clawhub search "learning" --limit 10
```

#### 安装技能
```bash
# 安装到默认位置
clawhub install learn-system-openclaw
```

#### 发布技能
```bash
# 从技能目录发布
cd learn-system-openclaw
clawhub publish .

# 或指定路径
clawhub publish /path/to/skill
```

#### 更新技能
```bash
# 更新所有已安装技能
clawhub update

# 更新指定技能
clawhub update learn-system-openclaw
```

#### 浏览最新技能
```bash
clawhub explore --limit 20
```

#### 认证管理
```bash
# 登录
clawhub login

# 检查当前登录状态
clawhub whoami

# 登出
clawhub logout
```

### GitHub 账号
- **GitHub**: https://github.com/code-firefly
- **使用场景**: ClawHub 发布技能时的账号关联

---

## GitHub CLI

用于管理 GitHub 仓库、Issues、PRs 等。

### 常用命令

#### 查看仓库
```bash
gh repo view code-firefly/my-claw-skills
```

#### 创建 Issue
```bash
gh issue create --title "Bug report" --body "Description"
```

#### 创建 Release
```bash
gh release create v1.0.0 --title "Release 1.0.0" --notes "Release notes"
```

#### 认证管理
```bash
# 查看认证状态
gh auth status

# 切换账户
gh auth switch --user code-firefly
```

---

## 技能开发工具

### 文件操作

#### jq - JSON 处理
```bash
# 读取 JSON
cat metadata.json | jq '.version'

# 更新 JSON
jq '.version = "1.0.1"' metadata.json > temp.json
mv temp.json metadata.json
```

### Git 操作

#### 查看状态
```bash
git status
git log --oneline -5
```

#### 提交变更
```bash
# 添加所有变更
git add .

# 提交
git commit -m "feat: add new skill"

# 推送
git push origin main
```

#### 创建 Tag
```bash
# 创建 tag
git tag v1.0.0

# 推送 tag
git push origin v1.0.0
```

### 技能验证

#### 验证 SKILL.md 格式
检查 frontmatter 是否完整：
```bash
# 检查 YAML frontmatter
head -20 SKILL.md

# 验证 JSON metadata
cat metadata.json | jq .
```

#### 验证技能结构
```bash
# 检查必需文件
ls -la SKILL.md VERSION metadata.json

# 检查子模块目录（如果存在）
ls -la modules/
```

---

## 自动化工具

### GitHub Actions

自动发布到 ClawHub 的工作流已配置：
- **文件**: `.github/workflows/release.yml`
- **触发**: Git tag push (v*)
- **功能**: 自动发布到 ClawHub 并创建 GitHub Release

### 推送脚本

手动推送脚本：
- **文件**: `push-to-github.sh`
- **用法**: `./push-to-github.sh`

---

*Keep this file updated with tool-specific notes and configurations.*
