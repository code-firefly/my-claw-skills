---
name: self-improvement
description: "捕获学习内容、错误和纠正，实现持续改进。适用于：命令失败、用户纠正、发现新能力需求、外部 API/工具异常、发现知识过时或错误、找到更好的方法。执行重要任务前也要回顾历史经验。Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks."
metadata:
---

# 持续改进技能 (Self-Improvement Skill)

将学习内容和错误记录到 Markdown 文件，实现持续改进。编码代理（coding agents）可以后续处理这些内容为修复，重要的学习内容会被提升到项目记忆（project memory）中。

## 快速参考 (Quick Reference)

| 情境 (Situation) | 操作 (Action) |
|-----------|--------|
| 命令/操作失败 (Command/operation fails) | 记录到 `.learnings/ERRORS.md` |
| 用户纠正你 (User corrects you) | 记录到 `.learnings/LEARNINGS.md`，分类为 `correction` |
| 用户想要缺失的功能 (User wants missing feature) | 记录到 `.learnings/FEATURE_REQUESTS.md` |
| API/外部工具失败 (API/external tool fails) | 记录到 `.learnings/ERRORS.md`，包含集成细节 |
| 知识过时 (Knowledge was outdated) | 记录到 `.learnings/LEARNINGS.md`，分类为 `knowledge_gap` |
| 发现更好的方法 (Found better approach) | 记录到 `.learnings/LEARNINGS.md`，分类为 `best_practice` |
| 简化/固化重复模式 (Simplify/Harden recurring patterns) | 记录/更新 `.learnings/LEARNINGS.md`，添加 `Source: simplify-and-harden` 和稳定的 `Pattern-Key` |
| 与现有条目相似 (Similar to existing entry) | 使用 `**See Also**` 链接，考虑提升优先级 |
| 广泛适用的学习 (Broadly applicable learning) | 提升到 `CLAUDE.md`、`AGENTS.md` 和/或 `.github/copilot-instructions.md` |
| 工作流改进 (Workflow improvements) | 提升到 `AGENTS.md`（OpenClaw 工作空间） |
| 工具陷阱 (Tool gotchas) | 提升到 `TOOLS.md`（OpenClaw 工作空间） |
| 行为模式 (Behavioral patterns) | 提升到 `SOUL.md`（OpenClaw 工作空间） |

## OpenClaw 设置（推荐）(OpenClaw Setup - Recommended)

OpenClaw 是此技能的主要平台。它使用基于工作空间的提示注入（workspace-based prompt injection）和自动技能加载（automatic skill loading）。

### 安装 (Installation)

**通过 ClawdHub（推荐）:**
```bash
clawdhub install self-improving-agent
```

**手动安装:**
```bash
git clone https://github.com/peterskoett/self-improving-agent.git ~/.openclaw/skills/self-improving-agent
```

从原始仓库改编为 OpenClaw 版本：https://github.com/pskoett/pskoett-ai-skills - https://github.com/pskoett/pskoett-ai-skills/tree/main/skills/self-improvement

### 工作空间结构 (Workspace Structure)

OpenClaw 将这些文件注入到每个会话（session）中：

```
~/.openclaw/workspace/
├── AGENTS.md          # 多代理工作流、委托模式 (Multi-agent workflows, delegation patterns)
├── SOUL.md            # 行为指导、个性、原则 (Behavioral guidelines, personality, principles)
├── TOOLS.md           # 工具能力、集成陷阱 (Tool capabilities, integration gotchas)
├── MEMORY.md          # 长期记忆（仅主会话）(Long-term memory - main session only)
├── memory/            # 每日记忆文件 (Daily memory files)
│   └── YYYY-MM-DD.md
└── .learnings/        # 此技能的日志文件 (This skill's log files)
    ├── LEARNINGS.md
    ├── ERRORS.md
    └── FEATURE_REQUESTS.md
```

### 创建学习文件 (Create Learning Files)

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

然后创建日志文件（或从 `assets/` 复制）：
- `LEARNINGS.md` — 纠正、知识差距、最佳实践
- `ERRORS.md` — 命令失败、异常
- `FEATURE_REQUESTS.md` — 用户请求的能力

### 提升目标 (Promotion Targets)

当学习内容被证明广泛适用时，将它们提升到工作空间文件：

| 学习类型 (Learning Type) | 提升到 (Promote To) | 示例 (Example) |
|---------------|------------|---------|
| 行为模式 (Behavioral patterns) | `SOUL.md` | "Be concise, avoid disclaimers"（简洁，避免免责声明） |
| 工作流改进 (Workflow improvements) | `AGENTS.md` | "Spawn sub-agents for long tasks"（为长任务派生子代理） |
| 工具陷阱 (Tool gotchas) | `TOOLS.md` | "Git push needs auth configured first"（Git push 需要先配置认证） |

### 会话间通信 (Inter-Session Communication)

OpenClaw 提供工具跨会话共享学习：

- **sessions_list** — 查看活动/最近的会话
- **sessions_history** — 读取另一个会话的转录
- **sessions_send** — 向另一个会话发送学习
- **sessions_spawn** — 为后台工作派生子代理

### 可选：启用 Hook (Optional: Enable Hook)

在会话开始时自动提醒：

```bash
# Copy hook to OpenClaw hooks directory
cp -r hooks/openclaw ~/.openclaw/hooks/self-improvement

# Enable it
openclaw hooks enable self-improvement
```

完整详情请参阅 `references/openclaw-integration.md`。

---

## 通用设置（其他代理）(Generic Setup - Other Agents)

对于 Claude Code、Codex、Copilot 或其他代理，在你的项目中创建 `.learnings/`：

```bash
mkdir -p .learnings
```

从 `assets/` 复制模板或创建带标题的文件。

### 添加引用到代理文件 (Add reference to agent files)

在 AGENTS.md、CLAUDE.md 或 .github/copilot-instructions.md 中添加引用，提醒自己记录学习（这是基于 hook 的提醒的替代方案）。

#### 持续改进工作流 (Self-Improvement Workflow)

当错误或纠正发生时：
1. 记录到 `.learnings/ERRORS.md`、`LEARNINGS.md` 或 `FEATURE_REQUESTS.md`
2. 审查并将广泛适用的学习提升到：
   - `CLAUDE.md` - 项目事实和约定
   - `AGENTS.md` - 工作流和自动化
   - `.github/copilot-instructions.md` - Copilot 上下文

## 记录格式 (Logging Format)

### 学习条目 (Learning Entry)

追加到 `.learnings/LEARNINGS.md`：

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement to make

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: simplify.dead_code | harden.input_validation (optional, for recurring-pattern tracking)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

### 错误条目 (Error Entry)

追加到 `.learnings/ERRORS.md`：

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
Brief description of what failed

### Error
```
Actual error message or output
```

### Context
- Command/operation attempted
- Input or parameters used
- Environment details if relevant

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001 (if recurring)

---
```

### 功能请求条目 (Feature Request Entry)

追加到 `.learnings/FEATURE_REQUESTS.md`：

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
What user wanted to do

### User Context
Why they needed it, what problem they're solving

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built, what it might extend

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## ID 生成 (ID Generation)

格式：`TYPE-YYYYMMDD-XXX`
- TYPE: `LRN`（学习）、`ERR`（错误）、`FEAT`（功能）
- YYYYMMDD: 当前日期
- XXX: 序号或随机的3个字符（如 `001`、`A7B`）

示例：`LRN-20250115-001`、`ERR-20250115-A3F`、`FEAT-20250115-002`

## 解决条目 (Resolving Entries)

当问题被修复时，更新条目：

1. 将 `**Status**: pending` 改为 `**Status**: resolved`
2. 在 Metadata 后添加解决块：

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: Brief description of what was done
```

其他状态值：
- `in_progress` - 正在积极处理
- `wont_fix` - 决定不解决（在 Resolution notes 中添加原因）
- `promoted` - 提升到 CLAUDE.md、AGENTS.md 或 .github/copilot-instructions.md

## 提升到项目记忆 (Promoting to Project Memory)

当学习内容广泛适用（不是一次性修复）时，将其提升到永久项目记忆。

### 何时提升 (When to Promote)

- 学习适用于多个文件/功能
- 任何贡献者（人类或 AI）都应该知道的知识
- 防止重复错误
- 记录项目特定的约定

### 提升目标 (Promotion Targets)

| 目标 (Target) | 适合的内容 (What Belongs There) |
|--------|-------------------|
| `CLAUDE.md` | 项目事实、约定、所有 Claude 交互的陷阱 |
| `AGENTS.md` | 代理特定的工作流、工具使用模式、自动化规则 |
| `.github/copilot-instructions.md` | GitHub Copilot 的项目上下文和约定 |
| `SOUL.md` | 行为指导、沟通风格、原则（OpenClaw 工作空间） |
| `TOOLS.md` | 工具能力、使用模式、集成陷阱（OpenClaw 工作空间） |

### 如何提升 (How to Promote)

1. **蒸馏**（Distill）学习为简洁的规则或事实
2. **添加**（Add）到目标文件的适当部分（如需要则创建文件）
3. **更新**（Update）原始条目：
   - 将 `**Status**: pending` 改为 `**Status**: promoted`
   - 添加 `**Promoted**: CLAUDE.md`、`AGENTS.md` 或 `.github/copilot-instructions.md`

### 提升示例 (Promotion Examples)

**学习**（冗长）:
> 项目使用 pnpm workspaces。尝试 `npm install` 但失败了。
> Lock file 是 `pnpm-lock.yaml`。必须使用 `pnpm install`。

**在 CLAUDE.md 中**（简洁）:
```markdown
## Build & Dependencies
- Package manager: pnpm (not npm) - use `pnpm install`
```

**学习**（冗长）:
> 修改 API 端点时，必须重新生成 TypeScript 客户端。
> 忘记这一点会导致运行时类型不匹配。

**在 AGENTS.md 中**（可操作）:
```markdown
## After API Changes
1. Regenerate client: `pnpm run generate:api`
2. Check for type errors: `pnpm tsc --noEmit`
```

## 重复模式检测 (Recurring Pattern Detection)

如果记录的内容与现有条目相似：

1. **先搜索**（Search first）：`grep -r "keyword" .learnings/`
2. **链接条目**（Link entries）：在 Metadata 中添加 `**See Also**: ERR-20250110-001`
3. **提升优先级**（Bump priority），如果问题持续发生
4. **考虑系统性修复**（Consider systemic fix）：重复问题通常表明：
   - 缺少文档（→ 提升到 CLAUDE.md 或 .github/copilot-instructions.md）
   - 缺少自动化（→ 添加到 AGENTS.md）
   - 架构问题（→ 创建技术债务 ticket）

## 简化与固化源 (Simplify & Harden Feed)

使用此工作流从 `simplify-and-harden` 技能摄入重复模式，并将它们转化为持久的提示指导。

### 摄入工作流 (Ingestion Workflow)

1. 从任务摘要读取 `simplify_and_harden.learning_loop.candidates`。
2. 对于每个候选项，使用 `pattern_key` 作为稳定的去重键。
3. 搜索 `.learnings/LEARNINGS.md` 中具有该键的现有条目：
   - `grep -n "Pattern-Key: <pattern_key>" .learnings/LEARNINGS.md`
4. 如果找到：
   - 增加 `Recurrence-Count`
   - 更新 `Last-Seen`
   - 添加相关条目/任务的 `See Also` 链接
5. 如果未找到：
   - 创建新的 `LRN-...` 条目
   - 设置 `Source: simplify-and-harden`
   - 设置 `Pattern-Key`、`Recurrence-Count: 1` 和 `First-Seen`/`Last-Seen`

### 提升规则（系统提示反馈）(Promotion Rule - System Prompt Feedback)

当所有条件都满足时，将重复模式提升到代理上下文/系统提示文件：

- `Recurrence-Count >= 3`
- 在至少 2 个不同任务中看到
- 在 30 天窗口内发生

提升目标：
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `SOUL.md` / `TOOLS.md` 用于 OpenClaw 工作空间级别的指导（如适用）

将提升的规则编写为简短的预防规则（在编码之前/期间做什么），而不是冗长的事件报告。

## 定期审查 (Periodic Review)

在自然断点处审查 `.learnings/`：

### 何时审查 (When to Review)
- 开始新的主要任务之前
- 完成功能之后
- 在有过去学习的领域工作时
- 活跃开发期间每周一次

### 快速状态检查 (Quick Status Check)
```bash
# Count pending items
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority items
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: backend" .learnings/*.md
```

### 审查操作 (Review Actions)
- 解决已修复的条目
- 提升适用的学习
- 链接相关条目
- 升级重复问题

## 检测触发器 (Detection Triggers)

当注意到以下情况时自动记录：

**纠正**（→ learning with `correction` category）:
- "不，那不对..."
- "实际上，应该是..."
- "你关于...错了"
- "那过时了..."

**功能请求**（→ feature request）:
- "你能也..."
- "我希望你能..."
- "有没有办法..."
- "为什么你不能..."

**知识差距**（→ learning with `knowledge_gap` category）:
- 用户提供你不知道的信息
- 你引用的文档过时
- API 行为与你的理解不同

**错误**（→ error entry）:
- 命令返回非零退出代码
- 异常或堆栈跟踪
- 意外的输出或行为
- 超时或连接失败

## 优先级指南 (Priority Guidelines)

| 优先级 (Priority) | 何时使用 (When to Use) |
|----------|-------------|
| `critical` | 阻止核心功能、数据丢失风险、安全问题 |
| `high` | 重大影响、影响常见工作流、重复问题 |
| `medium` | 中等影响、存在变通方法 |
| `low` | 轻微不便、边缘情况、锦上添花 |

## 区域标签 (Area Tags)

用于按代码库区域过滤学习：

| 区域 (Area) | 范围 (Scope) |
|------|-------|
| `frontend` | UI、组件、客户端代码 |
| `backend` | API、服务、服务端代码 |
| `infra` | CI/CD、部署、Docker、云 |
| `tests` | 测试文件、测试工具、覆盖率 |
| `docs` | 文档、注释、README |
| `config` | 配置文件、环境、设置 |

## 最佳实践 (Best Practices)

1. **立即记录**（Log immediately） - 上下文在问题之后最清晰
2. **具体**（Be specific） - 未来的代理需要快速理解
3. **包含重现步骤**（Include reproduction steps） - 特别是对于错误
4. **链接相关文件**（Link related files） - 使修复更容易
5. **建议具体修复**（Suggest concrete fixes） - 不仅仅是"调查"
6. **使用一致分类**（Use consistent categories） - 启用过滤
7. **积极提升**（Promote aggressively） - 如果不确定，添加到 CLAUDE.md 或 .github/copilot-instructions.md
8. **定期审查**（Review regularly） - 陈旧的学习会失去价值

## Gitignore 选项 (Gitignore Options)

**保持学习本地**（per-developer）:
```gitignore
.learnings/
```

**在仓库中跟踪学习**（team-wide）:
不要添加到 .gitignore - 学习成为共享知识。

**混合**（track templates, ignore entries）:
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Hook 集成 (Hook Integration)

通过代理 hook 启用自动提醒。这是**可选的**（opt-in） - 你必须显式配置 hooks。

### 快速设置（Claude Code / Codex）(Quick Setup)

在项目中创建 `.claude/settings.json`：

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }]
  }
}
```

这会在每个提示后注入学习评估提醒（~50-100 token 开销）。

### 完整设置（带错误检测）(Full Setup - With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/error-detector.sh"
      }]
    }]
  }
}
```

### 可用的 Hook 脚本 (Available Hook Scripts)

| 脚本 (Script) | Hook 类型 (Hook Type) | 目的 (Purpose) |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | 在任务后提醒评估学习 |
| `scripts/error-detector.sh` | PostToolUse (Bash) | 在命令错误时触发 |

详细配置和故障排除请参阅 `references/hooks-setup.md`。

## 自动技能提取 (Automatic Skill Extraction)

当学习内容足够有价值成为可重用技能时，使用提供的帮助程序提取它。

### 技能提取标准 (Skill Extraction Criteria)

当以下任何条件适用时，学习有资格进行技能提取：

| 标准 (Criterion) | 描述 (Description) |
|-----------|-------------|
| **重复**（Recurring） | 有到 2+ 相似问题的 `See Also` 链接 |
| **已验证**（Verified） | 状态是 `resolved`，有可工作的修复 |
| **非显而易见**（Non-obvious） | 需要实际调试/调查来发现 |
| **广泛适用**（Broadly applicable） | 非项目特定；跨代码库有用 |
| **用户标记**（User-flagged） | 用户说"保存为技能"或类似的话 |

### 提取工作流 (Extraction Workflow)

1. **识别候选**（Identify candidate）：学习符合提取标准
2. **运行帮助程序**（Run helper）（或手动创建）：
   ```bash
   ./skills/self-improvement/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improvement/scripts/extract-skill.sh skill-name
   ```
3. **自定义 SKILL.md**（Customize SKILL.md）：用学习内容填写模板
4. **更新学习**（Update learning）：将状态设置为 `promoted_to_skill`，添加 `Skill-Path`
5. **验证**（Verify）：在新会话中读取技能以确保它是自包含的

### 手动提取 (Manual Extraction)

如果你更喜欢手动创建：

1. 创建 `skills/<skill-name>/SKILL.md`
2. 使用 `assets/SKILL-TEMPLATE.md` 中的模板
3. 遵循 [Agent Skills spec](https://agentskills.io/specification)：
   - YAML frontmatter，包含 `name` 和 `description`
   - 名称必须匹配文件夹名称
   - 技能文件夹内没有 README.md

### 提取检测触发器 (Extraction Detection Triggers)

留意这些信号，表明学习应该成为技能：

**在对话中**:
- "Save this as a skill"
- "我总是遇到这个"
- "这对其他项目有用"
- "记住这个模式"

**在学习条目中**:
- 多个 `See Also` 链接（重复问题）
- 高优先级 + 已解决状态
- 分类：`best_practice`，具有广泛适用性
- 用户反馈赞扬解决方案

### 技能质量关口 (Skill Quality Gates)

提取前，验证：

- [ ] 解决方案已测试并工作
- [ ] 在没有原始上下文的情况下描述清晰
- [ ] 代码示例是自包含的
- [ ] 没有项目特定的硬编码值
- [ ] 遵循技能命名约定（小写、连字符）

## 多代理支持 (Multi-Agent Support)

此技能在不同的 AI 编码代理上工作，具有代理特定的激活。

### Claude Code

**激活**（Activation）：Hooks（UserPromptSubmit、PostToolUse）
**设置**（Setup）：`.claude/settings.json` 带有 hook 配置
**检测**（Detection）：通过 hook 脚本自动

### Codex CLI

**激活**（Activation）：Hooks（与 Claude Code 相同模式）
**设置**（Setup）：`.codex/settings.json` 带有 hook 配置
**检测**（Detection）：通过 hook 脚本自动

### GitHub Copilot

**激活**（Activation）：手动（无 hook 支持）
**设置**（Setup）：添加到 `.github/copilot-instructions.md`：

```markdown
## Self-Improvement

解决非显而易见的问题后，考虑记录到 `.learnings/`：
1. 使用 self-improvement 技能的格式
2. 使用 See Also 链接相关条目
3. 将高价值学习提升到技能

在聊天中询问："Should I log this as a learning?"
```

**检测**（Detection）：在会话结束时手动审查

### OpenClaw

**激活**（Activation）：工作空间注入 + 代理间消息
**设置**（Setup）：见上面的"OpenClaw 设置"部分
**检测**（Detection）：通过会话工具和工作空间文件

### 代理无关指导 (Agent-Agnostic Guidance)

无论代理如何，在以下情况应用持续改进：

1. **发现非显而易见的事情** - 解决方案不是即时的
2. **纠正自己** - 初始方法错了
3. **学习项目约定** - 发现未记录的模式
4. **遇到意外错误** - 特别是如果诊断困难
5. **找到更好的方法** - 改进原始解决方案

### Copilot Chat 集成 (Copilot Chat Integration)

对于 Copilot 用户，在相关时将其添加到提示中：

> 完成此任务后，评估是否应该使用 self-improvement 技能格式将任何学习记录到 `.learnings/`。

或使用快速提示：
- "记录到学习"
- "从解决方案创建技能"
- "检查 .learnings/ 中的相关问题"
