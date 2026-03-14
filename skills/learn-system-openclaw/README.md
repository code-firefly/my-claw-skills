# Learn System for OpenClaw

> 完整的学习管理系统，支持学习目标管理、课程学习、进度追踪、书签管理和知识缓存。

**返回**: [my-claw-skills](../) - OpenClaw 专用技能集合

---

## ✨ 特性

- 🎯 **学习目标管理** - 创建、追踪、切换、归档学习目标
- 📚 **课程管理** - 开始学习、完成课程、重置进度、课程路径映射
- 📊 **进度追踪** - 查看总体进度、查看课程详细状态、自动计算完成百分比
- 🔖 **书签系统** - 创建书签、继续书签、完成书签、探索笔记记录
- 💾 **知识缓存** - 初始化缓存、刷新缓存、查看缓存状态、优化参数支持

---

## 📦 安装

### 方式 1：通过 ClawHub 安装

```bash
clawhub install learn-system-openclaw
```

### 方式 2：手动安装

1. 将 `learn-system-openclaw` 目录复制到你的 OpenClaw skills 目录
2. 确保 `SKILL.md`、`VERSION` 和 `metadata.json` 文件完整
3. 重启 OpenClaw Gateway

---

## 🚀 快速开始

### 建议：创建专门的学习 Agent

⚠️ **重要提示**：本技能使用语义匹配来识别学习相关的查询。为了避免与其他技能发生冲突，**强烈建议**创建一个专门用于学习的 Agent：

```bash
# 创建专门的学习 Agent
openclaw agent create learning-agent --skills learn-system-openclaw

# 使用这个 Agent 处理所有学习相关的任务
openclaw session learning-agent
```

### 可能的语义冲突

由于本技能使用语义匹配，以下类型的查询可能会触发它：
- "学习这个 bug"（可能误触发学习系统）
- "学习这个文档"（如果只是想查看文档，不是学习）
- "我的学习计划"（如果只是记录，不是使用系统）

**解决方案**：
- 使用专门的学习 Agent（推荐）
- 使用更具体的关键词（例如"查看学习状态"而不是"我的学习"）
- 避免到误触发时，请反馈以帮助改进

---

## 📖 使用指南

### 创建学习目标

```
用户: 我要学 OpenClaw 技能开发
系统: 检测到"我要学"，引导创建学习目标
      → 询问学习目的、知识水平、期望时长等
      → 生成个性化课程结构
      → 保存到 .learn-system/goals.json
```

### 开始学习课程

```
用户: 开始学习第一个模块
系统: 显示课程进度概览
      → 引导用户开始第一个模块的学习任务
      → 记录开始时间
      → 更新 .learn-system/progress.json
```

### 查看学习状态

```
用户: 查看学习状态
系统: 从 .learn-system/progress.json 读取所有课程进度
      → 显示总体进度
      → 显示各优先级进度
      → 显示各课程详细状态
```

### 创建书签

```
用户: 创建书签 Tool Use 机制疑问
系统: 检测到"创建书签"，引导创建书签
      → 自动获取当前学习上下文
      → 记录疑问点
      → 保存到 .learn-system/bookmarks.json
```

### 继续书签

```
用户: 继续书签 Tool Use 机制疑问
系统: 从 .learn-system/bookmarks.json 读取书签
      → 显示探索目标和返回验证标准
      → 进入探索模式
```

### 完成书签

```
用户: 完成书签 Tool Use 机制疑问
系统: 更新 .learn-system/bookmarks.json
      → 将书签状态从 exploring 改为 completed
      → 记录完成时间
```

---

## 📂 目录结构

本技能使用 `.learn-system/` 作为根目录，避免与其他技能冲突：

```
<workspace>/
└── .learn-system/              # 项目级学习数据根目录
    ├── goals.json          # 所有学习目标（JSON）
    ├── progress.json       # 所有课程进度（JSON）
    ├── bookmarks.json     # 所有书签（JSON）
    └── cache/             # 课程资料缓存
        ├── <course-name>/   # 按课程组织的缓存
        │   ├── README.md
        │   ├── overview.md
        │   ├── concepts.md
        │   ├── guides.md
        │   └── .metadata.json
        └── .metadata.json     # 缓存索引
```

---

## 📋 触发关键词

### 主技能（语义匹配）
- "我要学" / "学习" / "开始学习" / "完成学习"
- "查看状态" / "学习状态" / "进度" / "学习进度"
- "创建书签" / "书签" / "继续书签" / "完成书签"
- "刷新缓存" / "缓存" / "知识缓存"

### 子模块（精确匹配）

#### 学习目标创建
- "创建学习目标" / "新建学习目标" / "添加学习目标"

#### 学习目标追踪
- "查看学习目标" / "显示学习目标" / "学习目标列表"
- "切换学习目标" / "激活学习目标" / "恢复学习目标"
- "暂停学习目标" / "停止学习目标"
- "归档学习目标" / "完成学习目标"

#### 课程管理
- "开始学习" / "开始课程" / "学习课程"
- "完成学习" / "完成课程" / "结束课程"
- "重置课程" / "重新开始课程"
- "新增课程" / "添加课程"

#### 学习状态管理
- "查看状态" / "显示状态" / "状态"
- "更新进度" / "学习进度"
- "查看进度" / "课程进度"

#### 书签管理
- "创建书签" / "添加书签" / "记笔记"
- "查看书签" / "书签列表" / "所有书签"
- "继续书签" / "探索书签"
- "完成书签" / "标记完成"

#### 学习工具集
- "初始化缓存" / "创建缓存" / "加载缓存"
- "刷新缓存" / "更新缓存"
- "查看缓存" / "缓存状态"
- "新增课程" / "添加课程" / "导入课程"

---

## ⚠️ 重要提示

### 路径控制

- **必须使用**：`.learn-system/` 作为根目录（相对于项目根）
- **禁止**：创建在其他位置（如项目根目录、全局目录）
- **必须**：创建文件前先使用 `exec mkdir -p .learn-system/<subdir>`

### 技能加载

- 由于技能加载机制问题，建议使用专门的学习 Agent
- 如果遇到技能未正确加载的问题，请重启 Gateway
- 建议定期重启 Gateway 以确保加载最新版本

### 语义匹配

- 本技能使用语义匹配，可能误触发
- 建议使用专门的学习 Agent 避免冲突
- 到误触发时请反馈以帮助改进

---

## 📚 文档索引

### 核心文档
- [SKILL.md](SKILL.md) - 主技能文件
- [CHANGELOG.md](CHANGELOG.md) - 更新日志
- [README.md](README.md) - 本文档

### 开发文档
- [docs/development/IMPLEMENTATION_GUIDE.md](docs/development/IMPLEMENTATION_GUIDE.md) - 实现指南
- [docs/development/CONTRIBUTING.md](docs/development/CONTRIBUTING.md) - 贡献指南

### 架构文档
- [docs/architecture/NEW_STRUCTURE.md](docs/architecture/NEW_STRUCTURE.md) - 新结构说明
- [docs/architecture/MIGRATION_GUIDE.md](docs/architecture/MIGRATION_GUIDE.md) - 迁移指南

### 运维文档
- [docs/operations/VERSION_CONTROL.md](docs/operations/VERSION_CONTROL.md) - 版本控制策略
- [docs/operations/NETWORK_TROUBLESHOOTING.md](docs/operations/NETWORK_TROUBLESHOOTING.md) - 网络故障排除

### 归档文档
- [docs/archives/bookmarks.md](docs/archives/bookmarks.md) - 书签文档归档

### 评测文档
- [docs/evaluation/v1.0.0-report.md](docs/evaluation/v1.0.0-report.md) - v1.0.0 评测报告

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目基于 Universal Learn Skills 转换整合，遵循原项目许可证。

---

## 🙏 致谢

基于以下 Universal Skills 转换整合：
- learn-goal-creator v1.0.0
- learn-goal-tracker v1.0.0
- learn-module-manager v1.0.0
- learn-status v1.0.0
- learn-tools v1.0.0

---

## 📞 联系方式

- **作者**: code-firefly
- **GitHub**: https://github.com/code-firefly/my-claw-skills
- **ClawHub**: https://clawhub.com/skills/learn-system-openclaw

---

*Version: 0.2.0-test*
*Last Updated: 2026-03-14*
