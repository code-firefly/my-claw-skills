# Skill Format Specification

## Universal Skill Format

Universal 格式是平台无关的技能定义格式，作为所有平台适配的上游源码。

### Directory Structure

```
skill-name/
├── SKILL.md         # 技能定义（必需）
├── VERSION          # 版本号（必需）
└── metadata.json    # 元数据（必需）
```

### SKILL.md Format

SKILL.md 是技能的核心定义文件，采用 Markdown 格式。

#### Frontmatter (Optional)

```yaml
---
name: "skill-name"
version: "1.0.0"
category: "learning"
description: "技能描述"
tags: ["tag1", "tag2"]
author: "作者名"
---
```

#### Content Sections

```markdown
# 技能名称

> 技能描述

## Description

详细描述技能的功能和使用场景。

## Trigger Keywords

- 关键词1
- 关键词2

## Behavior

描述技能的行为逻辑。

## Parameters

描述技能接受的参数。

## Examples

使用示例...
```

### VERSION Format

单行文本文件，包含语义化版本号：

```
1.0.0
```

版本号遵循 [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

### metadata.json Format

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "category": "learning|productivity|development",
  "description": "技能描述",
  "author": "作者名",
  "tags": ["tag1", "tag2"],
  "created_at": "2026-03-12",
  "platforms": {
    "universal": {
      "status": "supported",
      "tested_at": "2026-03-12",
      "notes": "平台无关的通用格式"
    },
    "claude-code": {
      "status": "supported|todo|not-planned|deprecated",
      "claude_code_version": "4.6.0",
      "model_version": "claude-sonnet-4-6",
      "tested_at": "2026-03-12",
      "notes": "适配说明"
    },
    "openclaw": {
      "status": "not-planned",
      "openclaw_version": null,
      "tested_at": null,
      "notes": ""
    }
  },
  "dependencies": [],
  "related_skills": ["related-skill-name"]
}
```

#### Platform Status Values

- `supported` - 已支持并测试
- `todo` - 计划适配
- `not-planned` - 不计划支持
- `deprecated` - 已废弃

## Platform-Specific Adaptations

### Claude Code

Claude Code 需要特定的 SKILL.md 格式：

1. **Frontmatter**: 必需，包含 `name`, `description`, `triggers`
2. **Trigger Format**: 使用 `triggers` 数组定义关键词
3. **Model Version**: 指定兼容的 Claude 模型

示例：

```yaml
---
name: learn-status
description: 学习状态管理技能
model: claude-sonnet-4-6
triggers:
  - 查看学习状态
  - 更新进度
  - 打勾
---
```

### OpenClaw

（待补充）

## Migration Guide

### 从 Claude Code 转换到 Universal

1. 提取核心逻辑（移除平台特定语法）
2. 统一 trigger 格式为列表
3. 创建 VERSION 和 metadata.json
4. 更新 PLATFORM_MATRIX.md

### 从 Universal 转换到 Claude Code

1. 添加必需的 frontmatter
2. 调整 trigger 格式
3. 添加平台特定功能
4. 更新 metadata.json 平台状态
5. 更新 PLATFORM_MATRIX.md

## Best Practices

1. **保持 Universal 格式纯净**: 不包含平台特定语法
2. **版本同步**: Universal 更新后，同步更新平台适配版本
3. **文档完整**: 每个变更都记录在 CHANGELOG.md
4. **测试覆盖**: 每个平台适配都需要测试

---

*Last Updated: 2026-03-12*
