# 迁移指南 - 从 v1.x 到 v2.0.0

> 升级 learn-system-openclaw 到新的项目级管理结构

**目标版本**：v2.0.0
**创建日期**：2026-03-13
**兼容性**：破坏性变更

---

## ⚠️ 重要说明

### 破坏性变更

v2.0.0 **不兼容** v1.x 的数据结构：

1. **目录结构变化**
   - 旧：`~/.learn-system/`（全局目录）
   - 新：`.learning/`（项目目录）

2. **文件格式变化**
   - 旧：多个 Markdown 文件和子目录
   - 新：单一 JSON 文件

3. **数据迁移**
   - 旧数据不会自动迁移
   - 需要手动或使用迁移脚本

### 建议

- ✅ **备份旧数据**：迁移前备份 `~/.learn-system/` 目录
- ✅ **创建新测试环境**：使用 `.learning/` 从头开始
- ✅ **验证功能后再迁移**：确保新结构工作正常

---

## 📁 目录结构对比

### v1.x 结构（旧）

```
~/.learn-system/                      # 全局目录
├── goals/
│   ├── active/
│   │   ├── learn-xxx.md
│   │   └── ...
│   ├── paused/
│   │   └── ...
│   ├── completed/
│   │   └── ...
│   └── archived/
│       └── ...
├── progress/
│   ├── PROGRESS.md
│   └── <course>-progress.md
├── bookmarks/
│   ├── LEARNING_BOOKMARKS.md
│   └── ...
├── courses/
│   ├── 01-基础入门/
│   │   └── <course>/
│   │       ├── course.md
│   │       ├── modules/
│   │       │   ├── 01-xxx/
│   │       │   │   ├── README.md
│   │       │   │   ├── checklist.md
│   │       │   │   └── notes.md
│   │       │   └── ...
│   │       └── resources/
│   │           ├── guides.md
│   │           └── exercises.md
│   └── ...
├── cache/
│   └── <course>-cache/
│       ├── knowledge/
│       │   ├── README.md
│       │   ├── overview.md
│       │   ├── concepts.md
│       │   ├── guides.md
│       │   └── .metadata.json
│       └── ...
└── active-goal.md
```

### v2.0.0 结构（新）

```
<workspace>/
└── .learning/                   # 项目目录
    ├── goals.json              # 所有学习目标
    ├── progress.json           # 所有课程进度
    ├── bookmarks.json         # 所有书签
    └── cache/                 # 课程缓存
        ├── <course-name>/     # 按课程
        │   ├── README.md
        │   ├── overview.md
        │   ├── concepts.md
        │   ├── guides.md
        │   └── .metadata.json
        └── .metadata.json     # 缓存索引
```

---

## 🔄 数据映射

### 学习目标映射

#### v1.x → v2.0.0

**源文件**：
- `goals/active/<goal-id>.md`
- `goals/paused/<goal-id>.md`
- `goals/completed/<goal-id>.md`
- `goals/archived/<goal-id>.md`

**目标文件格式**（旧）：
```markdown
# 学习目标：XXX

- **目标ID**: learn-xxx
- **创建时间**: 2026-03-XX
- **状态**: active | paused | completed | archived
- **类型**: theory | practice | mixed
...
```

**目标 JSON 格式**（新）：
```json
{
  "id": "learn-xxx",
  "name": "XXX",
  "status": "active",
  ...
}
```

**迁移逻辑**：
1. 读取所有子目录中的目标文件
2. 解析 Markdown 格式
3. 转换为 JSON 结构
4. 写入 `goals.json`

---

### 学习进度映射

#### v1.x → v2.0.0

**源文件**：
- `progress/PROGRESS.md`
- `<course>/notes.md`

**进度文件格式**（旧）：
```markdown
# 学习进度

## 课程：XXX

| ai-tools-fundamentals | P0 | 快速模式 | 进行中 | 0% |

## 学习日志
| 2026-03-07 | ai-tools-fundamentals | 开始学习 |
```

**进度 JSON 格式**（新）：
```json
{
  "courses": {
    "ai-tools-fundamentals": {
      "name": "XXX",
      "mode": "fast",
      "modules": {
        ...
      },
      "overall_progress": 0
    }
  }
}
```

**迁移逻辑**：
1. 读取 `PROGRESS.md` 解析课程进度
2. 读取各课程的 `notes.md` 获取模块进度
3. 合并为 JSON 结构
4. 写入 `progress.json`

---

### 书签映射

#### v1.x → v2.0.0

**源文件**：
- `bookmarks/LEARNING_BOOKMARKS.md`
- 各课程目录下的独立书签文件

**书签文件格式**（旧）：
```markdown
# 学习书签

## 🔵 探索中

### 1. Tool Use 机制

- **疑问点**: Tool Use 的具体实现原理是什么？
- **探索目标**: ...
```

**书签 JSON 格式**（新）：
```json
{
  "bookmarks": {
    "tool-use-questions": {
      "id": "tool-use-questions",
      "title": "XXX",
      "status": "exploring",
      ...
    }
  }
}
```

**迁移逻辑**：
1. 读取 `LEARNING_BOOKMARKS.md` 解析所有书签
2. 转换为 JSON 结构
3. 写入 `bookmarks.json`

---

### 课程缓存映射

#### v1.x → v2.0.0

**源目录**：
- `cache/<course>-cache/knowledge/`

**迁移逻辑**：
1. 复制整个 `<course>-cache/` 目录到 `.learning/cache/<course>/`
2. 更新 `.learning/cache/.metadata.json`

---

## 🛠️ 迁移步骤

### 步骤 1：备份旧数据

```bash
# 创建备份目录
mkdir -p ~/backup/learn-system-backup-$(date +%Y%m%d)

# 备份全局学习数据
cp -r ~/.learn-system ~/backup/learn-system-backup-$(date +%Y%m%d)/
```

### 步骤 2：提取学习目标

**手动方式**：
1. 打开 `~/.learn-system/goals/` 目录
2. 手动将各子目录中的目标文件整理到 JSON
3. 创建新项目的 `.learning/goals.json`

**脚本方式**（如果提供）：
```bash
# 运行迁移脚本
python migrate-goals.py ~/.learn-system/ <workspace>/.learning/
```

### 步骤 3：提取学习进度

**手动方式**：
1. 读取 `~/.learn-system/progress/PROGRESS.md`
2. 读取各课程的 `notes.md`
3. 整理为 `.learning/progress.json`

**脚本方式**（如果提供）：
```bash
python migrate-progress.py ~/.learn-system/ <workspace>/.learning/
```

### 步骤 4：提取书签

**手动方式**：
1. 读取 `~/.learn-system/bookmarks/LEARNING_BOOKMARKS.md`
2. 整理为 `.learning/bookmarks.json`

**脚本方式**（如果提供）：
```bash
python migrate-bookmarks.py ~/.learn-system/ <workspace>/.learning/
```

### 步骤 5：迁移课程缓存

```bash
# 复制缓存目录
cp -r ~/.learn-system/cache/ <workspace>/.learning/cache/

# 更新元数据
# 手动或脚本更新 .learning/cache/.metadata.json
```

### 步骤 6：验证新数据

```bash
# 进入项目目录
cd <workspace>

# 检查新结构
ls -la .learning/

# 验证 JSON 格式
cat .learning/goals.json | jq .
cat .learning/progress.json | jq .
cat .learning/bookmarks.json | jq .
```

### 步骤 7：测试功能

使用新技能测试所有功能：
- ✅ 创建学习目标
- ✅ 查看学习状态
- ✅ 创建书签
- ✅ 刷新缓存
- ✅ 更新进度

---

## 🧪 回滚方案

如果迁移出现问题或新版本不稳定：

### 快速回滚

```bash
# 恢复备份
rm -rf ~/.learn-system/
cp -r ~/backup/learn-system-backup-20260313/ ~/.learn-system/
```

### 使用旧版本技能

```bash
# 卸载新版本
clawhub uninstall learn-system-openclaw

# 安装旧版本
# 需要从 Git tag 或 GitHub Release 下载 v1.0.0
```

---

## 📋 迁移检查清单

### 准备阶段
- [ ] 备份 `~/.learn-system/` 目录
- [ ] 记录当前学习进度（截图或笔记）
- [ ] 关闭所有正在进行的课程会话

### 迁移阶段
- [ ] 迁移学习目标（goals）
- [ ] 迁移学习进度（progress）
- [ ] 迁移书签（bookmarks）
- [ ] 迁移课程缓存（cache）
- [ ] 创建 `.learning/.metadata.json`（如果需要）

### 验证阶段
- [ ] 验证 `.learning/goals.json` 格式正确
- [ ] 验证 `.learning/progress.json` 格式正确
- [ ] 验证 `.learning/bookmarks.json` 格式正确
- [ ] 验证 `.learning/cache/` 目录完整
- [ ] 检查缓存元数据正确

### 测试阶段
- [ ] 创建新学习目标测试
- [ ] 查看学习状态测试
- [ ] 创建书签测试
- [ ] 刷新缓存测试
- [ ] 更新进度测试

### 清理阶段
- [ ] 确认新版本工作正常
- [ ] 保留备份至少 1 周
- [ ] 更新文档和说明

---

## 🆘 故障排除

### 问题：JSON 解析错误

**症状**：`jq .` 报错

**原因**：JSON 格式不正确（缺少逗号、引号等）

**解决**：
1. 使用 JSON 验证工具检查格式
2. 手动修复格式错误
3. 或重新执行迁移脚本

### 问题：部分数据丢失

**症状**：某些目标或进度未迁移

**原因**：解析错误或遗漏某些文件

**解决**：
1. 检查备份中是否有遗漏的文件
2. 手动补充到新的 JSON 文件
3. 验证最终数据的完整性

### 问题：路径错误

**症状**：文件保存在错误的位置

**原因**：迁移脚本路径配置错误

**解决**：
1. 检查脚本中的路径配置
2. 手动移动文件到正确位置
3. 验证 `.learning/` 目录结构

---

## 📞 获取帮助

如果迁移过程中遇到问题：

1. **查看文档**
   - `NEW_STRUCTURE.md` - 新结构说明
   - `REFACTOR_PLAN.md` - 重构计划

2. **检查日志**
   - 查看技能执行日志
   - 查看错误信息

3. **回滚**
   - 使用备份恢复旧数据
   - 等待修复或使用迁移脚本

4. **反馈问题**
   - 在 ClawHub 或 GitHub 提交 Issue
   - 描述问题的详细信息

---

**文档版本**：1.0.0
**最后更新**：2026-03-13
**适用版本**：v2.0.0
