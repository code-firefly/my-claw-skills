# Text Summarizer - 评测示例

这是一个完整的 OpenClaw 技能评测示例，展示了如何使用 `skill-creator-op` 进行自动化评测。

## 技能概述

**技能名称**：text-summarizer-op
**功能**：智能文本摘要生成
**评测目标**：验证技能在不同文本类型（技术文档、博客、会议记录）下的摘要质量和触发准确性

## 评测准备状态

✅ **评测结构已准备**
- 目录结构：`eval-results/iteration-1/`
- 测试用例：4 个
- Baseline 目录：`eval-results/iteration-1/baseline/`
- With Skill 目录：`eval-results/iteration-1/with_skill/`

✅ **评测指令已生成**
- Baseline 评测指令：`eval-results/iteration-1/baseline_instructions.md`
- With Skill 评测指令：`eval-results/iteration-1/with_skill_instructions.md`
- 评分指令：`eval-results/iteration-1/grader_instructions.md`

## 测试用例

| ID | 名称 | 类型 | 预期 | 触发 |
|----|------|------|------|------|
| 1 | Technical Documentation Summary | 技术文档摘要 | 包含核心原则和最佳实践 | ✅ 是 |
| 2 | Blog Post Summary | 博客文章摘要 | 段落形式，包含主要观点 | ✅ 是 |
| 3 | Meeting Minutes Summary | 会议记录摘要 | 结构化格式，含议题和行动项 | ✅ 是 |
| 4 | Should Not Trigger - Code Request | 负面测试 | 不触发摘要技能，提供代码 | ❌ 否 |

## 运行评测

### 步骤 1：运行评测会话

使用 `sessions_spawn` 运行每个测试用例：

**有技能的版本：**
```bash
# 发送 with_skill_instructions.md 的内容给 agent
# Agent 会为每个测试用例调用 sessions_spawn
```

**Baseline 版本：**
```bash
# 发送 baseline_instructions.md 的内容给 agent
# Agent 会为每个测试用例调用 sessions_spawn（不带技能）
```

### 步骤 2：查看生成的结果

评测完成后，结果会保存在：
```
eval-results/iteration-1/
├── baseline/
│   ├── test_001/
│   │   ├── transcript.md
│   │   └── outputs/
│   ├── test_002/
│   │   └── ...
│   └── ...
├── with_skill/
│   ├── test_001/
│   │   ├── transcript.md
│   │   └── outputs/
│   ├── test_002/
│   │   └── ...
│   └── ...
└── ...
```

### 步骤 3：运行评分

发送 `grader_instructions.md` 的内容给 grader agent，它会：
1. 读取 `eval_set.json` 中的预期
2. 检查每个测试用例的 assertion
3. 生成 `grading.json` 文件

### 步骤 4：聚合结果

使用 `aggregate_benchmark.py` 聚合评测结果：

```bash
cd skills/text-summarizer-op
python3 ../skill-creator-op/scripts/aggregate_benchmark.py \
  eval-results/iteration-1 \
  --skill-name text-summarizer-op
```

这会生成：
- `eval-results/iteration-1/benchmark.json` - 评测数据
- `eval-results/iteration-1/benchmark.md` - 可读报告

### 步骤 5：查看结果

使用评测查看器：

```bash
python3 ../skill-creator-op/eval-viewer/generate_review.py \
  eval-results/iteration-1 \
  --skill-name "text-summarizer-op" \
  --benchmark eval-results/iteration-1/benchmark.json
```

## 手动快速测试

如果你想快速验证技能是否正常工作，可以手动运行：

```bash
# 创建一个子会话测试技能
sessions_spawn(
    task="帮我总结这段话：人工智能是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。这些任务包括学习、推理、问题解决、感知和语言理解。AI技术已经应用于医疗、金融、交通等多个领域。",
    runtime="acp",
    agentId="claude",
    mode="run",
    timeoutSeconds=60
)
```

## 评测断言说明

每个测试用例包含多个断言（assertions）：

- **content_check**：检查输出是否包含特定内容
- **format_check**：检查输出格式（段落、列表等）
- **length_check**：检查长度（句子数量、字数等）
- **negative_check**：确保输出不包含某类内容

评分时，agent 会根据断言类型使用不同的检查方法。

## 文件结构

```
text-summarizer-op/
├── SKILL.md                    # 技能定义
├── README.md                   # 本文件
├── evals/
│   └── evals.json             # 评测集定义
└── eval-results/
    └── iteration-1/
        ├── eval_set.json        # 评测集副本
        ├── baseline/           # Baseline 结果
        ├── with_skill/         # 带技能的结果
        ├── baseline_instructions.md
        ├── with_skill_instructions.md
        └── grader_instructions.md
```

## 下一步

1. ✅ **准备完成** - 评测环境已准备就绪
2. ⏳ **运行评测** - 使用 `sessions_spawn` 运行测试用例
3. ⏳ **评分结果** - 使用 grader agent 评分
4. ⏳ **查看报告** - 使用 generate_review.py 查看结果

## 注意事项

- 评测需要 ACP 已启用
- 默认使用 `claude` agent（可通过配置修改）
- 每个测试用例的超时时间默认为 300 秒
- 可以根据任务复杂度调整超时时间

## 相关文档

- [skill-creator-op 文档](../skill-creator-op/SKILL.md)
- [OpenClaw ACP 文档](https://docs.openclaw.ai/acp)
- [评测脚本使用说明](../skill-creator-op/scripts/run_eval_openclaw.py)
