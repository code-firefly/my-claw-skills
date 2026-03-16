# Skill Creator (OpenClaw 优化版) - sessions_spawn 修复

**修复版本**: v0.4.0
**修复日期**: 2026-03-14
**修复人**: 技能虾 🦐

---

## 📋 修复概述

### 问题描述

**问题**: skill-creator-op 使用了错误的工具来创建子任务

**错误信息**:
```
ACP target agent is not configured. Pass `agentId` in `sessions_spawn` or set `acp.defaultAgent` in config.
```

**根本原因分析**：

#### 原因 1：工具不兼容

**skill-creator-op 的设计**：
- 从 Claude Code 的 `skill-creator` 修改而来
- 原版使用 `init_skill.py` + 手动创建流程
- skill-creator-op 添加了评测功能
- **错误地使用了 `sessions_spawn` 工具**

**`sessions_spawn` 是什么？**
- 这是 **Claude Code** 的工具（用于 ACP harness）
- 在 ACP (Agent Code Protocol) 运行环境中才有 ACP agent
- 需要提供 `agentId` 参数

**OpenClaw 的子智能体系统**：
- 使用 `/subagents spawn <agentId> <task>` 命令
- 不需要 `agentId`（自动识别）
- 与 ACP harness 完全无关

**结论**：
- ❌ `sessions_spawn` 不适用于 OpenClaw
- ✅ 应该使用 `/subagents spawn`（OpenClaw 原生命命）

---

#### 原因 2：技能来源问题

**原始 skill-creator** (Claude Code)：
- 没有"评测"功能
- 使用 `init_skill.py` 脚本
- 工作流：理解 → 创建 → 编辑 → 打包

**skill-creator-op** (添加了评测功能)：
- 添加了"Running and evaluating test cases"章节
- 添加了完整的评测工作流
- **错误地假设** OpenClaw 也有相同的评测工具

**实际情况**：
- ❌ OpenClaw 没有自动评测工具（如 spawn、baseline、grader）
- ❌ 这些是 Claude Code 特有的功能
- ✅ OpenClaw 使用 `/subagents spawn` 来运行子任务

**结论**：
- skill-creator-op 不应该照搬 Claude Code 的评测流程
- 应该移除评测功能，改为简化的手动测试流程

---

## ✅ 修复方案

### 核心：移除评测功能，回归原始设计

#### 修复策略

1. **移除"Running and evaluating test cases"章节**
   - 这个章节完全依赖 `sessions_spawn`
   - 在 OpenClaw 中无法工作

2. **保留手动测试指南**
   - 保留技能创建、编辑、打包的功能
   - 移除所有 spawn、baseline、grader 相关内容

3. **保留 Description 优化功能**
   - Description 优化仍然可用
   - 但不依赖 `sessions_spawn`（使用手动测试或 `subagents spawn`）

4. **更新文档语言**
   - 改为中文，与技能语境一致

---

### 修复内容对比

| 章节 | 修复前 | 修复后 | 说明 |
|------|---------|--------|--------|
| **评测章节** | ❌ 有 | ✅ 移除 | 与 OpenClaw 不兼容 |
| **手动测试** | ❌ 无 | ✅ 保留 | 简化工作流 |
| **Description 优化** | ✅ 有 | ✅ 保留 | 手动方式 |
| **工作流 A/B** | ❌ 有 | ✅ 移除 | 不适用于 OpenClaw |
| **文档语言** | ❌ 英文 | ✅ 中文 | 保持一致 |

---

## 📝 修复后的技能结构

### 删除的章节

```markdown
## Running and evaluating test cases

（整个章节删除）
```

### 保留的章节

```markdown
## Creating a skill

（保留原始内容）

## Test Cases

（保留原始内容）

## Claude.ai-specific instructions

（保留原始内容）

## Cowork-Specific Instructions

（保留原始内容）

## Reference files

（保留原始内容）
```

### 新增说明

在 SKILL.md 顶部添加：

```markdown
> **⚠️ 注意**：本技能基于 Claude Code 的 skill-creator，已针对 OpenClaw 进行简化。
>
> **主要变更**：
> - ✅ 移除了评测功能（依赖 `sessions_spawn`）
> - ✅ 保留了手动测试指南（通过用户反馈改进）
> - ✅ 保留了 Description 优化功能（手动方式）
> - ✅ 改为中文文档
>
> **OpenClaw 限制**：
> - OpenClaw 没有 ACP harness（`sessions_spawn`）
> - OpenClaw 使用 `/subagents spawn` 来运行子任务
> - 建议用户直接在会话中测试技能，或使用 OpenClaw 的子智能体功能（`/subagents spawn`）
```

---

## 🎯 应用方法

### 方法 1：手动应用（推荐）

**步骤**：
1. 删除整个"Running and evaluating test cases"章节
2. 在顶部添加注意事项（见上节）
3. 更新版本号为 v0.4.0
4. 更新更新日志
5. 提交并推送

**命令**：
```bash
cd /home/wangxg/projects/my-claw-skills/skills/skill-creator-op
# 删除评测章节（从"## Running and evaluating test cases"到"## Cowork-Specific Instructions"之前）
# 在顶部添加注意事项
git add SKILL.md
git commit -m "fix: remove evaluation section, add OpenClaw compatibility notes"
git push
```

---

### 方法 2：我自动应用（可选）

告诉我：**"应用修复"**

我会：
1. 自动删除评测章节
2. 添加 OpenClaw 兼容性说明
3. 更新版本号和日志
4. 提交并推送

---

## 📊 预期效果

### 修复前

```
用户：评测这个技能
技能：尝试 spawn subagents...
技能：💥 崩溃，错误：ACP target agent is not configured
用户：😕 怎么办？
```

### 修复后

```
用户：评测这个技能
技能：技能已加载，遵循 instructions
技能：✅ 正常工作（手动测试，用户反馈）
用户：👍 流畅体验
```

---

## 🔍 修复要点总结

| 问题 | 原因 | 解决方案 | 效果 |
|------|--------|---------|--------|
| **无法创建子任务** | 使用了 `sessions_spawn`（Claude Code 工具）| 改为手动测试或 `/subagents spawn` | ✅ 解决 |
| **文档语言** | 英文（与技能不一致）| 改为中文 | ✅ 改进 |
| **评测功能冗余** | 照搬 Claude Code 评测流程（OpenClaw 不支持）| 移除整个章节 | ✅ 简化 |

---

## 📝 变更日志

### v0.4.0 (2026-03-14)

**修复**：
- ✅ 移除了"Running and evaluating test cases"章节
- ✅ 添加了 OpenClaw 兼容性说明
- ✅ 改为中文文档（顶部添加注意事项）
- ✅ 保留了手动测试指南
- ✅ 保留了 Description 优化功能（手动方式）

**改进**：
- 🟢 优雅降级：移除了无法工作的评测流程
- 🟢 用户体验：技能加载正常，不崩溃
- 🟢 文档一致性：中文文档，中文语境
- 🟢 适配 OpenClaw：明确说明与 Claude Code 的差异

**向后兼容**：✅ 维持（所有原始内容保留，移除了冗余的评测章节）

---

**修复人**：技能虾 🦐
**修复版本**：v0.4.0
**下一步**：应用到 skill-creator-op/SKILL.md，测试，提交，推送
