---
name: learn-system-openclaw
description: 完整的学习管理系统，支持学习目标管理、课程学习、进度追踪、书签管理和知识缓存。适用于学习目标创建、查看学习状态、开始学习课程、管理书签等相关场景。
subskills:
  - modules/goal-creator.md
  - modules/goal-tracker.md
  - modules/module-manager.md
  - modules/status.md
  - modules/tools.md
---

# 学习管理系统 (Learn System) v0.2.0

> 本技能提供完整的学习管理功能，包括目标创建、课程学习、进度追踪、书签管理和知识缓存。

**重要变更**：v0.2.0 采用项目级目录管理（`.learn-system/`），简化路径控制，增加强制性规则，确保路径 100% 有效。

---

## 🚨 强制性规则 ⚠️

以下规则**必须严格遵守**，违反将被视为技能执行失败：

### 路径规则

- **必须使用**：`.learn-system/` 作为根目录（相对于项目根）
- **禁止**：使用任何其他路径或让模型自主决定文件位置
- **要求**：任何文件操作前必须先检查目录是否存在

### 创建目录

- **必须**：创建文件前先使用 `exec mkdir -p .learn-system/<subdir>`
- **禁止**：假设目录已存在或跳过创建

### 错误处理

- 如果路径不符合预期，**必须**立即报错并停止
- 不得尝试"修复"或使用替代路径
- **禁止**：创建在其他位置（如项目根目录、全局目录）

---

## 🔐 强制性文件创建流程 ⚠️

### 步骤 1：确保基础目录存在

**在任何文件操作之前，必须执行以下命令**：

```bash
exec: mkdir -p .learning
```

**检查目录创建成功**：
```bash
exec: ls -la .learn-system/
```

**如果失败或目录不存在，必须报错并停止**：
```
❌ 错误：无法创建 .learn-system/ 目录
请检查权限或磁盘空间
```

---

### 步骤 2：确保子目录存在

**在执行特定功能前，必须确保相应的子目录存在**：

```bash
# 书签操作前
exec: mkdir -p .learn-system/cache

# 缓存操作前
exec: mkdir -p .learn-system/cache

# 进度操作前
exec: mkdir -p .learn-system/cache

# 课程缓存操作前
exec: mkdir -p .learn-system/cache/<course-name>
```

**禁止**：跳过以上任何步骤或使用其他路径。

---

### 步骤 3：验证目录结构

**在开始任何操作前，必须验证目录结构**：

```bash
exec: ls -la .learn-system/
```

**必须验证以下内容**：
- [ ] `.learn-system/` 目录存在
- [ ] `cache/` 子目录存在（如果需要）
- [ ] 目录权限正确（drwxr-xr-x）
- [ ] 没有其他异常文件

**如果验证失败，必须报错并停止**：
```
❌ 错误：目录结构验证失败
期望结构：.learn-system/cache/
实际结构：<实际 ls 结果>
```

---

## 📁 目录结构

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

**重要**：
- 使用 `.learn-system/` 作为所有路径的前缀
- 避免使用绝对路径或 `~` 符号
- 所有文件操作都必须先创建目录

---

## 🛠️ 禁止行为

以下操作**在任何情况下都不得执行**：

### 1. 禁止使用其他路径

- ❌ 在项目根目录创建文件
- ❌ 使用绝对路径到用户主目录
- ❌ 使用 `~/` 符号
- ❌ 使用全局 `~/.learn-system/` 路径
- ❌ 在其他位置创建任何文件

### 2. 禁止跳过目录创建

- ❌ 假设 `.learn-system/` 目录已存在
- ❌ 跳过 `exec mkdir -p .learn-system/<subdir>`
- ❌ 直接使用 `write` 或 `echo` 创建文件（必须先创建目录）

### 3. 禁止自主决定路径

- ❌ 让模型自主决定文件保存位置
- ❌ 使用任何非 `.learn-system/` 前缀的路径
- ❌ 询问用户"保存到哪"（必须使用 `.learn-system/`）

### 4. 禁止使用旧的目录结构

- ❌ 使用 `goals/active/` 等多目录结构
- ❌ 使用 `PROGRESS.md` 单文件
- ❌ 使用 `BOOKMARKS.md` 单文件
- ❌ 使用 `.learn-system/` 全局路径

---

## 🎯 强制性操作示例

### 正确的文件创建流程

```bash
# ✅ 正确：先创建目录，再写入文件
exec: mkdir -p .learn-system/cache/<course-name>
exec: cat > .learn-system/cache/<course-name>/README.md << 'EOF'
课程缓存内容
EOF
```

### 错误的文件创建流程

```bash
# ❌ 错误：直接写入，没有创建目录
exec: cat > .learn-system/cache/<course-name>/README.md << 'EOF'
课程缓存内容
EOF

# ❌ 错误：使用绝对路径
exec: mkdir -p ~/.learn-system/cache
exec: cat > ~/.learn-system/cache/README.md << 'EOF'
课程缓存内容
EOF
```

---

## 📋 操作检查清单

### 每次文件操作前必须检查

在执行任何文件操作（创建、读取、写入、更新）之前，**必须**确认：

- [ ] 已执行 `exec: mkdir -p .learning`
- [ ] 已验证 `.learn-system/` 目录存在
- [ ] 已验证子目录存在（如果需要）
- [ ] 使用 `.learn-system/` 前缀的路径
- [ ] 没有使用绝对路径或 `~` 符号

### 如果检查失败

必须立即报错并停止，不得继续执行。

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

### v0.2.0 (2026-03-13)

**重大变更**：
- 从全局目录（`~/.learn-system/`）切换为项目级目录（`.learn-system/`）
- 简化文件结构，使用 JSON 格式替代多目录结构
- 增加强制性规则，确保路径控制 100% 有效
- 优化子模块实现，简化逻辑

**破坏性变更**：
- 不兼容 v1.x 数据结构
- 需要手动迁移旧数据

**改进**：
- 路径控制 100% 有效，模型必须遵守强制性规则
- 代码更简洁，易于维护
- 符合项目隔离原则

---

*Version: 0.2.0*
*Created: 2026-03-13*
