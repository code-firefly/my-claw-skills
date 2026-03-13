# 更新日志 (Changelog)

本文档记录 learn-system-openclaw 的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)。

---

## [1.0.0] - 2026-03-13

### 新增 (Added)

- 🎉 **初始发布** - 统一学习管理系统
- ✨ 整合 5 个 Universal Learn Skills 为单个 OpenClaw Skill
- 📦 完整的学习目标管理功能
  - 创建学习目标（AI 引导）
  - 多目标追踪（active/paused/completed/archived）
  - 目标切换和状态管理
  - 聚焦视图显示
- 📚 课程管理功能
  - 开始学习（快速/完整模式选择）
  - 完成学习（验证完成度）
  - 重置课程（清除进度）
  - 课程路径映射和别名支持
- 📊 进度追踪功能
  - 查看总体进度
  - 查看课程详细状态
  - 自动计算完成百分比
  - PROGRESS.md 自动更新
- 🔖 书签系统
  - 创建书签（自动获取上下文）
  - 继续书签（探索模式）
  - 完成书签（返回主线）
  - 探索笔记记录
- 💾 知识缓存
  - 初始化缓存（拉取官方文档）
  - 刷新缓存（更新资料）
  - 查看缓存状态
  - 优化参数支持（retain_images=false, timeout=20）
- 🔧 课程管理工具
  - 新增课程
  - 更新课程信息
  - 删除课程

### 优化 (Changed)

- 🔄 统一语义意图识别机制
  - 主技能使用语义匹配
  - 子模块使用精确关键词匹配
- 📂 目录结构优化
  - 使用 `.learn-system/` 作为根目录
  - 避免与其他技能冲突
- 🇨🇳 完全中文界面
  - 所有关键词和提示均为中文
  - 面向中文用户优化

### 文档 (Documentation)

- 📖 完整的 SKILL.md（主技能说明）
- 📝 5 个子模块文档
- 📘 详细的 README.md（安装、使用指南）
- 📋 清晰的触发关键词列表
- ⚠️ 语义冲突提醒和建议

### 技术细节

- 🎯 意图识别与路由机制
  - "我要学 X" → 检查课程列表 → 路由到对应子模块
  - 智能别名解析（旧名称 → 新名称）
- 💡 行为规范
  - 书签探索模式（等待用户确认）
  - 理论知识分块展示（≤15行）
  - 用户确认机制

---

## [Unreleased]

### 计划中 (Planned)

- [ ] ClawHub 发布流程
- [ ] 真实环境测试
- [ ] 性能优化
- [ ] 更多学习资源模板
- [ ] 多语言支持（英文界面）

---

## 版本说明

### [1.0.0] - 2026-03-13

**重大里程碑**：首次发布，整合 5 个 Universal Skills 为单个统一的学习管理系统。

**从以下 Universal Skills 转换**：
- learn-goal-creator v1.0.0
- learn-goal-tracker v1.0.0
- learn-module-manager v1.0.0
- learn-status v1.0.0
- learn-tools v1.0.0

**转换策略**：
- 主技能（SKILL.md）提供意图识别和路由
- 5 个子模块（modules/*.md）提供具体功能
- 统一版本管理
- 独立发布

---

## 变更类型

- **新增 (Added)** - 新功能
- **变更 (Changed)** - 现有功能的变更
- **废弃 (Deprecated)** - 即将移除的功能
- **移除 (Removed)** - 已移除的功能
- **修复 (Fixed)** - Bug 修复
- **安全 (Security)** - 安全性修复

---

## 致谢

感谢以下项目的启发和支持：
- Universal Learn Skills (上游源码)
- OpenClaw (平台支持)
- ClawHub (技能分发平台)

---

*最后更新: 2026-03-13*
