---
name: skill-vetter
version: 1.0.0
description: 安全优先的技能审查工具。在安装任何技能前使用，检查红旗标记、权限范围和可疑模式。适用于从 ClawdHub、GitHub 或其他来源安装技能前的安全检查。Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.
---

# 技能审查工具 (Skill Vetter) 🔒

用于 AI 代理技能的安全优先审查协议。**未经审查绝不要安装技能。**

## 何时使用 (When to Use)

- 从 ClawdHub 安装任何技能之前
- 从 GitHub 仓库运行技能之前
- 评估其他代理共享的技能时
- 任何时候你被要求安装未知代码

## 审查协议 (Vetting Protocol)

### 步骤 1：来源检查 (Source Check)

```
需要回答的问题：
- [ ] 这个技能来自哪里？
- [ ] 作者是否知名/声誉良好？
- [ ] 有多少下载/星标？
- [ ] 上次更新是什么时候？
- [ ] 有其他代理的评论吗？
```

### 步骤 2：代码审查（强制）(Code Review - MANDATORY)

阅读技能中的所有文件。检查这些**红旗（RED FLAGS）**：

```
🚨 如果你看到以下内容，立即拒绝 (REJECT IMMEDIATELY IF YOU SEE)：
─────────────────────────────────────────
• curl/wget 到未知 URL
• 向外部服务器发送数据
• 请求凭证/令牌/API 密钥
• 在没有明确原因的情况下读取 ~/.ssh、~/.aws、~/.config
• 访问 MEMORY.md、USER.md、SOUL.md、IDENTITY.md
• 对任何内容使用 base64 解码
• 使用外部输入的 eval() 或 exec()
• 修改工作空间之外的系统文件
• 安装包而不列出它们
• 向 IP 而不是域名的网络调用
• 混淆代码（压缩、编码、缩小）
• 请求提升/sudo 权限
• 访问浏览器 cookie/会话
• 接触凭证文件
─────────────────────────────────────────
```

### 步骤 3：权限范围 (Permission Scope)

```
评估：
- [ ] 它需要读取什么文件？
- [ ] 它需要写入什么文件？
- [ ] 它运行什么命令？
- [ ] 它需要网络访问吗？到哪里？
- [ ] 范围对于其声明的目的来说是最小的吗？
```

### 步骤 4：风险分类 (Risk Classification)

| 风险等级 (Risk Level) | 示例 (Examples) | 操作 (Action) |
|------------|----------|--------|
| 🟢 低 (LOW) | 笔记、天气、格式化 | 基本审查，可以安装 |
| 🟡 中等 (MEDIUM) | 文件操作、浏览器、API | 需要完整的代码审查 |
| 🔴 高 (HIGH) | 凭证、交易、系统 | 需要人类批准 |
| ⛔ 极端 (EXTREME) | 安全配置、root 访问 | 不要安装 |

## 输出格式 (Output Format)

审查后，生成此报告：

```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [name]
Source: [ClawdHub / GitHub / other]
Author: [username]
Version: [version]
───────────────────────────────────────
METRICS:
• Downloads/Stars: [count]
• Last Updated: [date]
• Files Reviewed: [count]
───────────────────────────────────────
RED FLAGS: [None / List them]

PERMISSIONS NEEDED:
• Files: [list or "None"]
• Network: [list or "None"]  
• Commands: [list or "None"]
───────────────────────────────────────
RISK LEVEL: [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME]

VERDICT: [✅ SAFE TO INSTALL / ⚠️ INSTALL WITH CAUTION / ❌ DO NOT INSTALL]

NOTES: [Any observations]
═══════════════════════════════════════
```

## 快速审查命令 (Quick Vet Commands)

对于 GitHub 托管的技能：
```bash
# Check repo stats
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'

# List skill files
curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'

# Fetch and review SKILL.md
curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
```

## 信任层次 (Trust Hierarchy)

1. **官方 OpenClaw 技能** → 较低审查力度（仍需审查）
2. **高星标仓库（1000+）** → 中等审查力度
3. **已知作者** → 中等审查力度
4. **新/未知来源** → 最大审查力度
5. **请求凭证的技能** → 始终需要人类批准

## 记住 (Remember)

- 没有任何技能值得牺牲安全
- 有疑问，不要安装
- 要求人类做出高风险决策
- 记录你审查的内容以供将来参考

---

*偏执是一种特性。*（Paranoia is a feature.）🔒🦀
