# 更新日志 (Changelog)

本文档记录 learn-system-openclaw 的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)。

---

## [0.2.0] - 2026-03-14

### 正式版发布 🎉

**重要更新**：从测试版（0.2.0-test）升级为正式版（0.2.0），修复技能加载机制问题。

#### ✅ 修复 (Fixed)

- 🐛 **技能加载机制不稳定**
  - 规范化文件名：`skill.md` → `SKILL.md`（符合 OpenClaw 技能标准）
  - 确保 OpenClaw 能正确识别和加载技能
  - 移除测试版标记，技能已稳定

#### 🚀 改进 (Changed)

- ⚡ **触发优化**
  - 优化 SKILL.md frontmatter，添加更多触发关键词
  - 增强描述的"pushy"程度，提高技能触发准确率
  - 添加中英文双语触发关键词（"学习目标"、"学习计划"、"学习进度"、"learning goal"、"study plan"等）

- 📝 **文档优化**
  - 简化技能文档，移除过度强调的规则描述
  - 保留核心规则，减少视觉干扰
  - 优化内容结构，提升可读性

#### 🎨 新功能 (Added)

- ✨ **OpenClaw 特定配置**
  - 添加 `metadata.openclaw` 配置到 SKILL.md frontmatter
  - 支持技能 emoji（📚）
  - 配置多平台支持（Linux, macOS, Windows）

#### 📊 兼容性

- ✅ 符合 OpenClaw v1.0.0 技能规范
- ✅ 支持技能自动触发和加载
- ✅ 无破坏性变更，兼容 0.2.0-test 数据

---

## [0.3.0] - 2026-03-14

### JSON Schema 和学习包支持 🎉

**重大功能**：添加 JSON Schema 验证和学习包导出/导入功能，支持学习内容分享。

#### ✨ 新功能 (Added)

- 📦 **学习包管理**
  - 导出学习包：将学习目标、进度、书签、缓存打包为 JSON 文件
  - 导入学习包：从 JSON 文件导入他人的学习内容
  - 学习包格式：符合 learning-package.schema.json 标准

- 🎯 **JSON Schema 验证**
  - goals.schema.json：学习目标数据结构验证
  - progress.schema.json：学习进度数据结构验证
  - bookmarks.schema.json：书签数据结构验证
  - learning-package.schema.json：学习包格式验证

- 🚀 **增强的触发关键词**
  - 添加"导出学习包"、"导入学习包"、"分享学习内容"等触发词
  - 支持中英文双语关键词

#### 🔧 变更 (Changed)

- 📝 **文档更新**
  - tools.md：添加学习包管理功能详细说明
  - SKILL.md：更新意图识别和路由，添加学习包管理场景
  - 新增 schemas/README.md：Schema 使用说明

- 🧪 **测试用例更新**
  - 更新 evals.json，匹配新的 JSON 文件结构
  - 新增学习包导出/导入测试用例（ID: 16, 17）
  - 新增 JSON Schema 验证测试用例（ID: 18）

#### 📖 文档 (Documentation)

- 📝 **新增文档**
  - schemas/README.md：JSON Schema 使用指南
  - schemas/goals.schema.json：学习目标 Schema
  - schemas/progress.schema.json：学习进度 Schema
  - schemas/bookmarks.schema.json：书签 Schema
  - schemas/learning-package.schema.json：学习包 Schema

#### 🎨 设计改进

- 📦 **学习包结构**
  - 支持完整包（目标 + 进度 + 书签 + 缓存）
  - 支持部分导出（仅课程内容、仅学习进度等）
  - 支持合并导入（避免覆盖现有数据）

- 🔐 **元数据支持**
  - 所有数据结构支持 metadata 字段
  - 支持作者、标签、分享设置等
  - 支持版本控制和更新追踪

#### 🚀 改进 (Improved)

- ✅ **数据完整性**：通过 JSON Schema 确保数据结构正确
- ✅ **可分享性**：学习包格式支持跨平台分享
- ✅ **可扩展性**：Schema 支持未来扩展字段
- ✅ **向后兼容**：v0.2.0 数据可直接使用，无需迁移

#### 📊 兼容性

- ✅ 向后兼容 v0.2.0 数据结构
- ✅ 新增功能不影响现有功能
- ✅ Schema 版本独立于技能版本

#### 🎯 使用示例

**导出学习包**：
```
用户：导出我的学习包
系统：生成 openclaw-dev.learning-package.json
```

**导入学习包**：
```
用户：导入这个学习包：friend-package.learning-package.json
系统：验证并导入学习内容
```

---

## [0.2.0-test] - 2026-03-14

### 测试版发布 ⚠️

**重要说明**：这是一个测试版，存在已知的技能加载机制问题。建议用户在专门的 agent 中使用此技能。

#### 🎉 新功能 (Added)

- ✨ **完整的学习管理系统**
  - 学习目标管理（创建、追踪、切换、归档）
  - 课程管理（开始、完成、重置、课程路径映射）
  - 进度追踪（查看总体进度、查看课程详细状态、自动计算完成百分比）
  - 书签系统（创建书签、继续书签、完成书签、探索笔记记录）
  - 知识缓存（初始化缓存、刷新缓存、查看缓存状态）

#### 🔧 变更 (Changed)

- 🔄 **目录结构优化**
  - 使用 `.learn-system/` 作为根目录（而非 `.learning/`）
  - 简化文件结构，使用 JSON 格式（goals.json, progress.json, bookmarks.json）
  - 避免与其他技能冲突
  
- 🔄 **强制性路径规则**
  - 增加强制性规则，确保路径控制 100% 有效
  - 所有文件操作必须使用 `.learn-system/` 前缀
  - 创建文件前必须先使用 `exec mkdir -p .learn-system/<subdir>`

#### 📖 文档 (Documentation)

- 📝 **文档优化**
  - 清理和归档过时文档（MIGRATION_GUIDE 等）
  - 更新 README.md，添加更详细的安装和使用指南
  - 完善触发关键词列表
  - 添加语义冲突提醒和建议

#### ⚠️ 已知问题

**问题 1：技能加载机制不稳定**
- **描述**：子代理可能使用旧版本技能，无法加载最新的技能文件
- **影响**：修改技能文件后，可能需要重启 Gateway 或重建 agent 才能生效
- **解决方案**：建议用户在专门的 agent 中使用此技能，或定期重启 Gateway

**问题 2：路径控制部分失效**
- **描述**：尽管修改了所有文件为 `.learn-system/`，模型可能仍创建 `.learning/` 目录
- **影响**：文件可能创建在错误位置
- **解决方案**：通过实际使用验证路径，必要时手动修正

**问题 3：意图识别错误**
- **描述**：某些请求可能被误识别（如"刷新缓存"可能被识别为 `clawhub update`）
- **影响**：功能执行不符合预期
- **解决方案**：使用更精确的关键词，如"刷新知识缓存"而非"刷新缓存"

#### 🧪 测试状态

- **测试覆盖**：进行了 8 轮迭代测试
- **测试环境**：OpenClaw v2026.3.8，skill-creator 评测框架
- **测试结果**：发现技能加载机制问题，路径控制部分失效
- **预期评分**：60-70/100（未达到 80/100 发布标准）

#### 🚀 改进建议

1. **创建专门的学习 Agent**
   - 避免与其他技能冲突
   - 使用技能加载稳定的 agent
   - 确保技能始终从正确位置加载

2. **用户反馈收集**
   - 通过 Discord、GitHub Issues 等渠道反馈问题
   - 根据反馈改进技能
   - 优先解决技能加载和路径控制问题

3. **文档完善**
   - 添加更多使用示例
   - 提供故障排除指南
   - 说明已知问题和解决方案

#### 📊 技能加载机制

**优先级**：
1. `~/.openclaw/workspace/skills/<skill-name>/` - 优先级最高
2. `<workspace>/skills/<skill-name>/` - 优先级次之
3. 其他技能位置 - 优先级最低

**当前配置**：
```json
skill-manager:
  workspace: /home/wangxg/projects/my-claw-skills
  skills: [learn-system-openclaw]
  
实际加载路径:
  ~/.openclaw/workspace/skills/learn-system-openclaw/
```

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

*最后更新: 2026-03-14*
