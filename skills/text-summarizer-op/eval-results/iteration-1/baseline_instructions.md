# Evaluation Instructions: baseline

**Skill:** text-summarizer-op
**Output Directory:** eval-results/iteration-1

## Task

For each test case below, spawn an OpenClaw sub-session and run the prompt. Save the results to the specified directory.

## Session Spawn Parameters

- Use `runtime="acp"`
- Use `mode="run"` (one-shot execution)
- Set appropriate `timeoutSeconds` based on the task complexity (default: 300)

- Run without the skill (baseline)

## Test Cases

### Test 1: Technical Documentation Summary

**Prompt:** 帮我总结一下这段技术文档：

# REST API 设计指南

RESTful API 是一种软件架构风格，用于设计网络应用程序。它基于 HTTP 协议，使用标准方法如 GET、POST、PUT、DELETE 来操作资源。

## 核心原则

1. **无状态性**：每个请求都包含所有必要信息
2. **统一接口**：使用标准化的 URL 和方法
3. **可缓存**：响应可以被缓存以提高性能
4. **分层系统**：客户端不知道是否连接到终端服务器

## 最佳实践

- 使用名词而不是动词设计 URL（如 /users 而不是 /getUsers）
- 使用 HTTP 状态码表示操作结果
- 实现 CORS 以支持跨域请求
- 使用 HTTPS 保证传输安全

## 总结

遵循 REST 原则可以创建可扩展、易维护的 API。

**Expected Output:** 包含核心原则（无状态性、统一接口、可缓存、分层系统）和最佳实践（URL设计、状态码、CORS、HTTPS）的摘要，长度3-5句话

**Save Results To:** `eval-results/iteration-1/baseline/test_001/`
- `transcript.md` - Full conversation transcript
- `outputs/` - Any generated files

```markdown
# How to run this test case

Use sessions_spawn with the following parameters:

```
sessions_spawn(
    task="帮我总结一下这段技术文档：

# REST API 设计指南

RESTful API 是一种软件架构风格，用于设计网络应用程序。它基于 HTTP 协议，使用标准方法如 GET、POST、PUT、DELETE 来操作资源。

## 核心原则

1. **无状态性**：每个请求都包含所有必要信息
2. **统一接口**：使用标准化的 URL 和方法
3. **可缓存**：响应可以被缓存以提高性能
4. **分层系统**：客户端不知道是否连接到终端服务器

## 最佳实践

- 使用名词而不是动词设计 URL（如 /users 而不是 /getUsers）
- 使用 HTTP 状态码表示操作结果
- 实现 CORS 以支持跨域请求
- 使用 HTTPS 保证传输安全

## 总结

遵循 REST 原则可以创建可扩展、易维护的 API。",
    runtime="acp",
    mode="run",
    timeoutSeconds=300,
    cwd="eval-results/iteration-1/baseline/test_001",
)
```

Then save the transcript and outputs.

---

### Test 2: Blog Post Summary

**Prompt:** 请摘要这篇博客文章：

# 为什么学习编程很重要

编程已经成为现代社会的一项基础技能，类似于阅读和写作。在数字化时代，掌握编程能力可以带来多方面的优势。

## 提升问题解决能力

编程训练逻辑思维和系统性思考。当你面对一个复杂问题时，编程教会你如何将其分解为小的、可管理的步骤。这种思维方式在其他领域同样适用。

## 增强职业竞争力

无论在哪个行业，编程技能都是加分项。从金融到医疗，从教育到娱乐，数字化转型正在改变所有行业。懂编程的人更容易适应这种变化。

## 创造力和表达力

编程也是一种创造性的表达方式。通过代码，你可以将想法变为现实，构建有用的工具、游戏或应用。这种创造力是非常有成就感的。

## 结论

学习编程不仅仅是为了成为程序员，更是为了在数字时代保持竞争力。无论你的职业目标是什么，编程技能都会为你打开新的可能性。

**Expected Output:** 包含问题解决能力、职业竞争力、创造力和表达力三个主要观点的摘要，段落形式

**Save Results To:** `eval-results/iteration-1/baseline/test_002/`
- `transcript.md` - Full conversation transcript
- `outputs/` - Any generated files

```markdown
# How to run this test case

Use sessions_spawn with the following parameters:

```
sessions_spawn(
    task="请摘要这篇博客文章：

# 为什么学习编程很重要

编程已经成为现代社会的一项基础技能，类似于阅读和写作。在数字化时代，掌握编程能力可以带来多方面的优势。

## 提升问题解决能力

编程训练逻辑思维和系统性思考。当你面对一个复杂问题时，编程教会你如何将其分解为小的、可管理的步骤。这种思维方式在其他领域同样适用。

## 增强职业竞争力

无论在哪个行业，编程技能都是加分项。从金融到医疗，从教育到娱乐，数字化转型正在改变所有行业。懂编程的人更容易适应这种变化。

## 创造力和表达力

编程也是一种创造性的表达方式。通过代码，你可以将想法变为现实，构建有用的工具、游戏或应用。这种创造力是非常有成就感的。

## 结论

学习编程不仅仅是为了成为程序员，更是为了在数字时代保持竞争力。无论你的职业目标是什么，编程技能都会为你打开新的可能性。",
    runtime="acp",
    mode="run",
    timeoutSeconds=300,
    cwd="eval-results/iteration-1/baseline/test_002",
)
```

Then save the transcript and outputs.

---

### Test 3: Meeting Minutes Summary

**Prompt:** 帮我整理会议纪要的要点：

# 产品周会纪要

时间：2024年3月15日
参会人员：产品团队全体成员

## 议题讨论

### 新功能开发
- 用户反馈显示移动端体验需要改进
- 计划在下个版本增加深色模式
- 性能优化列为高优先级任务

### 市场推广
- 与社交媒体平台合作计划已启动
- 预算分配：广告60%，内容创作30%，活动10%
- 目标：下月用户增长20%

### 技术债务
- 重构遗留代码工作已完成60%
- 需要额外的2周时间完成剩余部分
- 建议暂停新功能开发直到重构完成

## 行动项
1. 张三：完成深色模式设计稿（本周内）
2. 李四：制定社交媒体合作方案（下周前）
3. 王五：安排技术债务评审会议（下周一）

**Expected Output:** 结构化摘要，包含议题讨论要点和行动项

**Save Results To:** `eval-results/iteration-1/baseline/test_003/`
- `transcript.md` - Full conversation transcript
- `outputs/` - Any generated files

```markdown
# How to run this test case

Use sessions_spawn with the following parameters:

```
sessions_spawn(
    task="帮我整理会议纪要的要点：

# 产品周会纪要

时间：2024年3月15日
参会人员：产品团队全体成员

## 议题讨论

### 新功能开发
- 用户反馈显示移动端体验需要改进
- 计划在下个版本增加深色模式
- 性能优化列为高优先级任务

### 市场推广
- 与社交媒体平台合作计划已启动
- 预算分配：广告60%，内容创作30%，活动10%
- 目标：下月用户增长20%

### 技术债务
- 重构遗留代码工作已完成60%
- 需要额外的2周时间完成剩余部分
- 建议暂停新功能开发直到重构完成

## 行动项
1. 张三：完成深色模式设计稿（本周内）
2. 李四：制定社交媒体合作方案（下周前）
3. 王五：安排技术债务评审会议（下周一）",
    runtime="acp",
    mode="run",
    timeoutSeconds=300,
    cwd="eval-results/iteration-1/baseline/test_003",
)
```

Then save the transcript and outputs.

---

### Test 4: Should Not Trigger - Code Request

**Prompt:** 帮我写一个 Python 函数来排序数组

**Expected Output:** 不触发摘要技能，提供代码实现

**Save Results To:** `eval-results/iteration-1/baseline/test_004/`
- `transcript.md` - Full conversation transcript
- `outputs/` - Any generated files

```markdown
# How to run this test case

Use sessions_spawn with the following parameters:

```
sessions_spawn(
    task="帮我写一个 Python 函数来排序数组",
    runtime="acp",
    mode="run",
    timeoutSeconds=300,
    cwd="eval-results/iteration-1/baseline/test_004",
)
```

Then save the transcript and outputs.

---
