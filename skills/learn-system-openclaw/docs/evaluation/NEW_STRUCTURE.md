# 新的目录结构 - learn-system-openclaw v2.0.0

> 项目级学习管理，简化路径，强制控制

**版本**：2.0.0
**创建日期**：2026-03-13
**状态**：设计中

---

## 📁 新的目录结构

### 根目录

```
<workspace>/
└── .learn-system/              # 项目级学习数据根目录
```

**说明**：
- 使用 `.learn-system/` 作为相对根目录（相对于项目根）
- 避免全局 `~/.learn-system/` 的路径控制问题
- 每个项目独立管理学习数据

### 子目录结构

```
.learn-system/
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
    └── .metadata.json   # 缓存索引
```

---

## 📄 文件说明

### goals.json

**目的**：存储所有学习目标及其状态

**结构**：
```json
{
  "version": "2.0.0",
  "active_goal_id": "learn-docker",
  "goals": {
    "learn-docker": {
      "id": "learn-docker",
      "name": "学习 Docker 容器技术",
      "status": "active",  // active | paused | completed | archived
      "type": "mixed",  // theory | practice | mixed
      "created_at": "2026-03-08",
      "paused_at": null,
      "completed_at": null,
      "description": "掌握 Docker 容器化和编排技能",
      "priority": "P1",
      "estimated_duration": "1-2周",
      "course_name": "docker-fundamentals"
    }
  }
}
```

**优点**：
- 单一文件，易于读取和更新
- JSON 结构，程序化访问友好
- 避免复杂的目录结构

---

### progress.json

**目的**：存储所有课程的学习进度

**结构**：
```json
{
  "version": "2.0.0",
  "active_goal_id": "learn-docker",
  "courses": {
    "docker-fundamentals": {
      "name": "Docker 容器基础",
      "priority": "P1",
      "mode": "full",  // fast | full
      "started_at": "2026-03-08",
      "completed_at": null,
      "current_module": "镜像管理",
      "modules": {
        "基础入门": {
          "status": "completed",  // not_started | in_progress | completed
          "completed_at": "2026-03-09"
        },
        "镜像管理": {
          "status": "in_progress",
          "completed_at": null
        },
        "容器部署": {
          "status": "not_started",
          "completed_at": null
        },
        "Docker Compose": {
          "status": "not_started",
          "completed_at": null
        }
      },
      "overall_progress": 25  // 百分比
    }
  }
}
```

**优点**：
- 单一文件存储所有进度
- 易于计算总体进度
- 支持多课程并行学习

---

### bookmarks.json

**目的**：存储所有书签及其状态

**结构**：
```json
{
  "version": "2.0.0",
  "bookmarks": {
    "tool-use-questions": {
      "id": "tool-use-questions",
      "title": "Tool Use 机制疑问",
      "course": "ai-tools-fundamentals",
      "module": "第一部分 > 架构与概念",
      "question": "Tool Use 的具体实现原理是什么？",
      "status": "completed",  // exploring | completed
      "created_at": "2026-03-07",
      "completed_at": "2026-03-09",
      "exploration_goals": [
        "阅读官方 Tool Use 文档",
        "查看 Tool Use 的源码实现"
      ],
      "exploration_notes": "...",
      "return_criteria": [
        "能够解释 Tool Use 的工作原理"
      ]
    }
  }
}
```

**优点**：
- 单一文件管理所有书签
- 易于按状态、课程、模块筛选
- 支持探索记录和验证标准

---

### cache/ 目录

**目的**：存储课程知识缓存

**结构**：
```
cache/
├── <course-name>/      # 按课程组织
│   ├── README.md       # 缓存说明
│   ├── overview.md     # 概述内容
│   ├── concepts.md     # 核心概念
│   ├── guides.md       # 使用指南
│   └── .metadata.json  # 缓存元数据
└── .metadata.json     # 缓存索引
```

**.metadata.json 示例**：
```json
{
  "version": "2.0.0",
  "courses": {
    "ai-tools-fundamentals": {
      "cache_date": "2026-03-07",
      "source_urls": [
        "https://code.claude.com/docs",
        "https://github.com/anthropics/claude-code"
      ],
      "files": [
        "overview.md",
        "concepts.md",
        "guides.md"
      ],
      "version": "1.0"
    }
  }
}
```

**优点**：
- 按课程组织，易于管理
- 支持多课程缓存
- 保留缓存元数据和版本信息

---

## 🔄 路径规则

### 基础路径

所有路径**必须**使用 `.learn-system/` 作为根目录（相对于项目根）。

### 相对路径示例

| 功能 | 旧路径（v1.0） | 新路径（v2.0） |
|------|------------------|----------------|
| 读取目标 | `.learn-system/goals/active/xxx.md` | `.learn-system/goals.json` |
| 创建书签 | `.learn-system/bookmarks/LEARNING_BOOKMARKS.md` | `.learn-system/bookmarks.json` |
| 读取进度 | `.learn-system/progress/PROGRESS.md` | `.learn-system/progress.json` |
| 课程缓存 | `.learn-system/cache/<course>/xxx.md` | `.learn-system/cache/<course>/xxx.md` |

### 强制性规则

- ✅ **必须**：使用 `.learn-system/` 作为所有路径的前缀
- ❌ **禁止**：使用任何其他路径或让模型自主决定
- ✅ **必须**：文件操作前先创建目录
- ✅ **必须**：使用相对路径（非绝对路径）

---

## 📊 对比分析

### v1.0 结构的问题

1. **路径控制失败**
   - 使用 `~/.learn-system/` 全局路径
   - 模型不遵循路径说明
   - 试过多种修复均失败

2. **目录过于复杂**
   - goals/ 下有 4 个子目录（active, paused, completed, archived）
   - 每个目标一个文件，难以管理
   - 进度分散在多个课程目录中

3. **文件操作复杂**
   - 需要理解复杂的目录结构
   - 文件路径长且易错
   - 维护成本高

### v2.0 结构的优势

1. **路径控制有效**
   - 使用简单的相对路径 `.learn-system/`
   - JSON 格式，单一文件操作
   - 易于验证和测试

2. **结构简化**
   - 4 个主要文件（goals, progress, bookmarks, cache）
   - cache/ 下按课程组织
   - 层次清晰，易于理解

3. **易于程序化访问**
   - JSON 格式，易于解析
   - 单一文件操作，减少 I/O
   - 支持脚本化和自动化

---

## 🛠️ 迁移指南

详见：`MIGRATION_GUIDE.md`

---

**最后更新**：2026-03-13
**设计者**：技能虾 (skill-manager agent)
