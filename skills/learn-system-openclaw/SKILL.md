---
name: learn-system-openclaw
description: 完整的学习管理系统，支持学习目标管理、课程学习、进度追踪、书签管理、知识缓存和学习包导出/导入。**确保在以下场景使用此技能**：当用户提到"学习目标"、"创建学习计划"、"查看学习进度"、"学习 X 课程"、"记录学习书签"、"课程缓存"、"学习计划"、"学习进度"、"书签"、"导出学习包"、"导入学习包"、"分享学习内容"、"使用学习包"等学习管理相关的请求时，即使用户没有明确说"使用学习管理系统"也必须调用此技能。同时支持中文和英文关键词。
subskills:
  - modules/goal-creator.md
  - modules/goal-tracker.md
  - modules/module-manager.md
  - modules/status.md
  - modules/tools.md
metadata:
  {
    "openclaw": {
      "requires": {},
      "primaryEnv": null,
      "os": ["linux", "darwin", "win32"],
      "emoji": "📚"
    }
  }
---

# 学习管理系统 (Learn System) v0.3.0

> 本技能提供完整的学习管理功能，包括目标创建、课程学习、进度追踪、书签管理、知识缓存和学习包导出/导入。

**重要特性**：
- ✅ 项目级目录管理（`.learn-system/`），避免全局路径冲突
- ✅ JSON 格式数据存储，结构化且易于维护
- ✅ 完整的子技能支持（目标创建、追踪、模块管理、状态查询、书签和缓存）
- ✅ 符合 OpenClaw 技能规范，支持自动触发和加载

---

## 🔐 核心规则

为了确保技能稳定运行，请遵循以下规则：

### 路径规范

- **统一使用**：`.learn-system/` 作为根目录（相对于项目根）
- **创建前检查**：任何文件操作前先检查目录是否存在
- **先创建后使用**：使用 `exec mkdir -p .learn-system/<subdir>` 创建目录

### 目录结构

```
.learn-system/
├── goals.json      # 学习目标
├── progress.json   # 课程进度
├── bookmarks.json  # 学习书签
└── cache/         # 课程资料缓存
```

---

## 📁 完整目录结构

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

## 🔄 意图识别与路由

当检测到学习相关的语义时，按以下逻辑路由到对应的子模块：

### 1. 学习目标相关

- **创建学习目标**：当用户说"我要学 X"且 X 不在现有课程列表中时
- **查看学习目标**：查询所有目标概览
- **切换/暂停/恢复学习目标**：管理目标状态

→ 路由到 `modules/goal-creator.md` 或 `modules/goal-tracker.md`

### 2. 课程学习相关

- **开始学习**：当用户说"我要学 X"且 X 在现有课程列表中时
- **完成学习**：标记课程为已完成
- **重置课程**：清除课程进度

→ 路由到 `modules/module-manager.md`

### 3. 学习状态相关

- **查看学习状态**：查看所有课程进度概览
- **更新进度**：更新特定课程的进度
- **课程进度**：查看特定课程的详细进度

→ 路由到 `modules/status.md`

### 4. 书签管理相关

- **创建书签**：记录学习中的疑问点
- **继续书签**：回到之前的书签继续探索
- **完成书签**：标记书签为已完成
- **删除书签**：移除不需要的书签

→ 路由到 `modules/tools.md`

### 5. 知识缓存相关

- **刷新缓存**：更新课程知识缓存
- **查看缓存**：查看缓存状态
- **知识缓存**：管理课程资料缓存

→ 路由到 `modules/tools.md`

### 6. 学习包管理相关

- **导出学习包**：分享学习内容（目标、进度、书签、缓存）
- **导入学习包**：使用他人分享的学习包
- **学习包**：管理学习包的导出和导入

→ 路由到 `modules/tools.md`

---

## 📝 使用建议

### 项目隔离

每个项目有独立的 `.learn-system/` 目录，不同项目的学习数据互不干扰。

### 推荐工作流

1. 在项目根目录使用技能
2. 所有学习数据保存在 `.learn-system/` 目录
3. 使用 JSON 文件管理数据
4. 缓存保存在 `.learn-system/cache/` 目录

### 语义匹配

本技能使用语义意图匹配。为了避免误触发，建议使用具体的关键词：
- "创建学习目标"而不是"创建目标"
- "查看学习状态"而不是"查看状态"
- "学习 Docker"（明确学习主题）

**已知限制**：
- "学习这个 bug"可能误触发（调试场景）
- 建议使用专门的学习 Agent 避免冲突

---

## 📊 数据格式

### goals.json

```json
{
  "version": "0.2.0",
  "active_goal_id": "learn-docker",
  "goals": {
    "learn-docker": {
      "id": "learn-docker",
      "name": "学习 Docker 容器技术",
      "status": "active",
      "type": "mixed",
      "created_at": "2026-03-08",
      "description": "掌握 Docker 容器化和编排技能",
      "priority": "P1",
      "course_name": "docker-fundamentals"
    }
  }
}
```

### progress.json

```json
{
  "version": "0.2.0",
  "active_goal_id": "learn-docker",
  "courses": {
    "docker-fundamentals": {
      "name": "Docker 容器基础",
      "priority": "P1",
      "mode": "full",
      "started_at": "2026-03-08",
      "completed_at": null,
      "current_module": "镜像管理",
      "modules": {
        "基础入门": { "status": "completed" },
        "镜像管理": { "status": "in_progress" },
        "容器部署": { "status": "not_started" },
        "Docker Compose": { "status": "not_started" }
      },
      "overall_progress": 25
    }
  }
}
```

### bookmarks.json

```json
{
  "version": "0.2.0",
  "bookmarks": {
    "tool-use-questions": {
      "id": "bookmark-1234567890",
      "title": "Tool Use 机制疑问",
      "course": "ai-tools-fundamentals",
      "module": "第一部分 > 架构与概念",
      "question": "Tool Use 的具体实现原理是什么？",
      "status": "completed",
      "created_at": "2026-03-07",
      "completed_at": "2026-03-09",
      "exploration_goals": [
        "阅读官方 Tool Use 文档",
        "查看 Tool Use 的源码实现"
      ],
      "exploration_notes": "",
      "return_criteria": [
        "能够解释 Tool Use 的工作原理"
      ]
    }
  }
}
```

---

## 📋 更新日志

### v0.2.0 (2026-03-14)

**正式版发布**：
- 从测试版（0.2.0-test）升级为正式版（0.2.0）
- 规范化文件名：`skill.md` → `SKILL.md`（符合 OpenClaw 技能标准）
- 优化 SKILL.md frontmatter，添加更多触发关键词
- 添加 OpenClaw 特定 metadata 配置
- 简化技能文档，移除过度强调的规则描述

**触发优化**：
- 增强描述的"pushy"程度，提高技能触发准确率
- 添加中英文双语触发关键词
- 明确列出触发场景，减少误触发

**兼容性**：
- 符合 OpenClaw v1.0.0 技能规范
- 支持多平台（Linux, macOS, Windows）

**改进**：
- 技能文档更简洁易读
- 核心规则保留，但减少视觉干扰
- 符合项目隔离原则

---

*Version: 0.2.0*
*Created: 2026-03-13*
*Updated: 2026-03-14*
