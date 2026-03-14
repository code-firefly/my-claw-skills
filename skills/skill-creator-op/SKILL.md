---
name: skill-creator-op
description: 创建、修改和测试 OpenClaw 技能，优化技能性能和描述触发准确率。适用于从头创建技能、编辑现有技能、运行评估测试、基准测试性能，或优化技能描述以提高触发准确率。每当用户提到技能开发、创建技能、优化技能、技能测试、描述优化或技能性能分析时，都应该使用此技能，即使用户没有明确要求。
---

# Skill Creator (OpenClaw Optimized)

> **⚠️ OpenClaw 兼容性说明**：
> 本技能是从 Claude Code 的 `skill-creator` 修改而来，已针对 OpenClaw 进行适配。
>
> **主要变更**：
> - ✅ 评测功能使用 OpenClaw 的 `sessions_spawn`（runtime="acp"）代替 Claude Code 的 `claude -p`
> - ✅ 支持通过 `sessions_spawn` 创建独立的评测会话
> - ✅ 保留了 Description 优化功能
> - ✅ 改为中文文档（顶部添加注意事项）
>
> **前置条件**：
> 1. **ACP 已启用**：检查 ACP 配置是否启用
>    ```bash
>    openclaw config get acp
>    ```
>    确保 `"enabled": true`
>
> 2. **默认 Agent 配置**：查看默认使用的 agent
>    ```bash
>    openclaw config get acp.defaultAgent
>    ```
>    通常是 `claude`。如果需要使用其他 agent（如 `skill-manager`），需将其添加到 `acp.allowedAgents`：
>    ```bash
>    openclaw config set acp.allowedAgents '["pi","claude","codex","opencode","gemini","kimi","skill-manager"]'
>    ```
>
> 3. **允许的 Agents**：查看当前允许的 agent 列表
>    ```bash
>    openclaw config get acp.allowedAgents
>    ```
>
> **OpenClaw 评测支持**：
> - OpenClaw 支持 ACP harness，通过 `sessions_spawn` 创建子会话
> - 支持指定 `agentId`（默认使用配置中的 `acp.defaultAgent`，通常是 `claude`）
> - 支持线程绑定的持久会话（`thread: true, mode: "session"`）
> - 支持一次性运行（`mode: "run"`）或持久会话
>
> **评测脚本适配**：
> - 原始评测脚本（run_eval.py）基于 `claude -p`，需要适配 OpenClaw
> - 可以使用 `sessions_spawn` 工具创建评测会话
> - 建议创建 OpenClaw 特定的评测脚本（run_eval_openclaw.py）

**原始版本**：`skill-creator` (Universal AgentSkills 格式)

---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, process of creating a skill goes like this:

- Decide what you want skill to do and roughly how it should do it
- Write a draft of skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help to user evaluate results both qualitatively and quantitatively
  - While runs happen in background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to user (or if they already existed, explain ones that already exist)
  - Use `eval-viewer/generate_review.py` script to show to user results for them to look at, and also let them look at quantitative metrics
- Rewrite to skill based on feedback from user's evaluation of results (and also if there are any glaring flaws that become apparent from quantitative benchmarks)
- Repeat until you're satisfied
- Expand to test set and try again at larger scale

Your job when using this skill is to figure out where to user is in this process and then jump in and help them progress through these stages. So for instance, maybe they're like "I want to make a skill for X". You can help narrow down what they mean, write a draft, write to test cases, figure out how they want to evaluate, run all to prompts, and repeat.

On other hand, maybe they already have a draft of skill. In this case you can go straight to eval/iterate part of loop.

Of course, you should always be flexible and if to user is like "I don't need to run a bunch of evaluations, just vibe with me", you can do that instead.

Then after to skill is done (but again, order is flexible), you can also run to skill description improver, which we have a whole separate script for, to optimize triggering of to skill.

Cool? Cool.

## Communicating with to user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. If you haven't heard (and how could you, it's only very recently that it started), there's a trend now where to power of Claude is inspiring plumbers to open up their terminals, parents and grandparents to google "how to install npm". On other hand, bulk of users are probably fairly computer-literate.

So please pay attention to context cues to understand how to phrase your communication! In to default case, just to give you some idea:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from to user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if to user will get it.

**Chinese Context Awareness:**

When communicating with Chinese users, be aware of:
- Mixed language usage: Many Chinese developers mix Chinese and English technical terms naturally
- Cultural preferences: Chinese users may prefer more structured, step-by-step explanations
- Technical terminology: Some terms have direct Chinese equivalents (e.g., "脚本" for script, "部署" for deploy), but English terms are often preferred in technical contexts
- Communication style: Be explicit and thorough; Chinese users often appreciate detailed explanations with clear rationales

**When to user uses mixed language (e.g., "帮我 create 个 dashboard"):**
- Mirror their language pattern appropriately
- Don't "correct" their language - they're communicating effectively
- Technical terms in English are fine and often preferred
- Use the language they use for key concepts

**Example responses:**
- User: "帮我优化这个 skill 的 description"
- You: "好的，我来帮你优化技能描述。优化 description 可以提高触发准确率..."

- User: "I want to run evals 测试这个技能"
- You: "我来帮你设置评估测试。Evals 可以帮助我们发现技能的..."

---

## Creating a skill

### Capture Intent

Start by understanding to user's intent. The current conversation might already contain a workflow to user wants to capture (e.g., they say "turn this into a skill"). If so, extract answers from conversation history first — to tools used, to sequence of steps, corrections to user made, input/output formats observed. The user may need to fill to gaps, and should confirm before proceeding to to next step.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's to expected output format?
4. Should we set up test cases to verify to skill works? Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from test cases. Skills with subjective outputs (writing style, art) often don't need them. Suggest to appropriate default based on to skill type, but let to user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs - if useful for research (searching docs, finding similar skills, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on to user.

### Write to SKILL.md

Based on to user interview, fill in these components:

- **name**: Skill identifier
- **description**: When to trigger, what it does. This is to primary triggering mechanism - include both what to skill does AND specific contexts for when to use it. All "when to use" info goes here, not in to body. Note: currently Claude has a tendency to "undertrigger" skills -- to not use them when they'd be useful. To combat this, please make to skill descriptions a little bit "pushy". So for instance, instead of "How to build a simple fast dashboard to display internal Anthropic data.", you might write "How to build a simple fast dashboard to display internal Anthropic data. Make sure to use this skill whenever to user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"
- **compatibility**: Required tools, dependencies (optional, rarely needed)
- **the rest of to skill :)**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading)

These word counts are approximate and you can feel free to go longer if needed.

**Key patterns:**
- Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of hierarchy along with clear pointers about where to model using to skill should go next to follow up.
- Reference files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

**Domain organization**: When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only to relevant reference file.

#### Principle of Lack of Surprise

This goes without saying, but skills must not contain malware, exploit code, or any content that could compromise system security. A skill's contents should not surprise to user in their intent if described. Don't go along with requests to create misleading skills or skills designed to facilitate unauthorized access, data exfiltration, or other malicious activities. Things like a "roleplay as an XYZ" are OK though.

#### Writing Patterns

Prefer using imperative form in instructions.

**Defining output formats** - You can do it like this:
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern** - It's useful to include examples. You can format them like this (but if "Input" and "Output" are in examples you might want to deviate a little):
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

#### Advanced Configuration (OpenClaw Specific)

OpenClaw provides additional configuration options beyond to standard AgentSkills format.

**Skill Gating (Metadata)** - Use `metadata.openclaw.requires` to filter skills at load time:

```yaml
---
name: my-skill
description: Use this tool
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["uv"], "env": ["API_KEY"], "config": ["browser.enabled"] },
        "primaryEnv": "API_KEY",
        "os": ["linux", "darwin"],
      },
  }
---
```

**Metadata fields:**
- `requires.bins` - List of binaries that must exist in PATH
- `requires.anyBins` - List where at least one binary must exist in PATH
- `requires.env` - List of environment variables that must exist (or be provided in config)
- `requires.config` - List of openclaw.json config paths that must be truthy
- `primaryEnv` - Environment variable name to associate with `skills.entries.<name>.apiKey`
- `os` - OS restrictions (darwin, linux, win32)
- `emoji` - Optional emoji for macOS Skills UI
- `homepage` - Optional URL for macOS Skills UI
- `install` - Optional installer specs (brew/node/go/download)

**Environment Variable Injection** - Configure in `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    entries: {
      "my-skill": {
        enabled: true,
        apiKey: "KEY_HERE",
        env: {
          API_KEY: "KEY_HERE",
        },
        config: {
          endpoint: "https://example.invalid",
          model: "custom-model",
        },
      },
    },
  },
}
```

**Configuration keys:**
- `enabled: false` - Disable this skill even if it's built-in/installed
- `env` - Environment variables injected for agent runs (only if not already set)
- `apiKey` - Convenience field for skills declaring `primaryEnv`
- `config` - Custom skill-specific settings

**Skill Loading Priority** - Skills load from three locations (highest to lowest):

1. `<workspace>/skills` - Workspace-specific skills (highest priority)
2. `~/.openclaw/skills` - Local/managed skills (medium priority)
3. Built-in skills - Shipped with OpenClaw package (lowest priority)

If to same skill name exists in multiple locations, to highest priority version wins. You can add additional directories via `skills.load.extraDirs` in `~/.openclaw/openclaw.json`.

**Publishing to ClawHub** - Share your skills with to community:

```bash
# From to skill directory
cd my-skill
clawhub publish .

# Or specify path
clawhub publish /path/to/skill
```

Before publishing, ensure:
- SKILL.md follows to format
- description is optimized for triggering
- All required files are included
- Version is updated (if modifying existing skill)
- Test cases demonstrate to skill works

**Best Practices for Chinese Context:**

1. **Bilingual Descriptions** - Include both Chinese and English trigger phrases in description:
   ```yaml
   description: 创建仪表盘和可视化。Use this whenever 用户提到仪表盘、数据可视化、内部指标或想要显示公司数据。Even when user uses English terms like dashboard, charts, metrics.
   ```

2. **Chinese Examples** - Include realistic Chinese prompts in test cases:
   ```json
   {
     "prompt": "老板发了个 excel 文件要我加个利润率列，收入在 C 列成本在 D 列",
     "expected_output": "Excel file with profit margin column added"
   }
   ```

3. **Cultural Considerations** - Be aware of common Chinese technical terminology:
   - "脚本" vs "脚本文件"
   - "部署" vs "上线"
   - "接口" vs "API"
   - "插件" vs "plugin"
   - "技能" vs "skill"

4. **Mixed Language Support** - Users often mix Chinese and English:
   - "帮我 create 个 dashboard"
   - "把数据 export 到 CSV"
   - "需要 run 个 script"

Design skills to handle these mixed-language inputs gracefully.

### Writing Style

Try to explain to model why things are important in lieu of heavy-handed MUSTs. Use theory of mind and try to make to skill general and not super-narrow to specific examples. Start by writing a draft and then look at it with fresh eyes and improve it.

### Test Cases

After writing to skill draft, come up with 2-3 realistic test prompts — to kind of thing a real user would actually say. Share them with to user: [you don't have to use this exact language] "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

**For Chinese context, create test cases in multiple language patterns:**

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    },
    {
      "id": 2,
      "prompt": "帮我处理这个数据文件，导出成 CSV 格式",
      "expected_output": "Data processed and exported as CSV",
      "files": ["data.xlsx"]
    },
    {
      "id": 3,
      "prompt": "Create a script to backup to database daily",
      "expected_output": "Python/bash script for daily database backup",
      "files": []
    },
    {
      "id": 4,
      "prompt": "老板要我搞个自动化脚本，每天备份数据库",
      "expected_output": "自动化脚本，每天执行数据库备份",
      "files": []
    }
  ]
}
```

Save test cases to `evals/evals.json`. Don't write assertions yet — just to prompts. You'll draft assertions in to next step while to runs are in progress.

See `references/schemas.md` for to full schema (including to `assertions` field, which you'll add later).

---

## Running Evaluations with OpenClaw

OpenClaw provides `sessions_spawn` to create isolated sub-sessions for evaluation. This is different from Claude Code's `claude -p` approach.

### Using sessions_spawn for Eval

You can spawn a sub-session with the skill loaded to run test cases:

```python
# Example: Spawn a sub-session to test a skill
# This is done via the sessions_spawn tool, not via a Python script
sessions_spawn(
    task="Use the my-skill to process this request",
    runtime="acp",  # Use ACP harness
    agentId="claude",  # Optional: specify agent (uses acp.defaultAgent if omitted)
    mode="run",  # One-shot execution
    timeoutSeconds=300
)
```

**Key differences from Claude Code:**
- OpenClaw uses the `sessions_spawn` tool directly (no CLI command equivalent to `claude -p`)
- Eval sessions are created within the current OpenClaw session
- Results come back as agent responses, not CLI output
- Transcript can be retrieved via `sessions_history`

### OpenClaw Eval Workflow

1. **Create test directory structure:**
   ```
   eval-results/
   ├── iteration-1/
   │   ├── baseline/
   │   │   └── test_001/
   │   │       ├── transcript.md
   │   │       └── outputs/
   │   └── with_skill/
   │       └── test_001/
   │           ├── transcript.md
   │           └── outputs/
   ```

2. **Spawn eval sessions:**
   For each test case, spawn a sub-session with or without the skill:

   ```json
   // evals/evals.json
   {
     "skill_name": "my-skill",
     "evals": [
       {
         "id": 1,
         "prompt": "Process this file",
         "expected_output": "CSV file with processed data",
         "files": ["input.xlsx"],
         "should_trigger": true
       }
     ]
   }
   ```

3. **Run grader:**
   Use the grader agent to evaluate outputs:
   ```bash
   python scripts/run_eval_openclaw.py \
     --eval-set evals/evals.json \
     --skill-path . \
     --output-dir eval-results/iteration-1
   ```

### Creating OpenClaw Eval Scripts

The original `run_eval.py` is designed for Claude Code's `claude -p`. For OpenClaw, use the new `run_eval_openclaw.py` script that:

1. Prepares the directory structure for evaluations
2. Generates instructions for the agent to spawn sessions
3. Provides grader instructions for evaluation

### Using run_eval_openclaw.py

The OpenClaw eval workflow is a 3-step process:

**Step 1: Prepare eval structure**
```bash
python scripts/run_eval_openclaw.py \
  --prepare \
  --eval-set evals/evals.json \
  --output-dir eval-results/iteration-1
```

This creates the directory structure with baseline/ and with_skill/ directories for each test case.

**Step 2: Spawn evaluation sessions**

Generate spawn instructions:
```bash
python scripts/run_eval_openclaw.py \
  --action spawn-instructions \
  --eval-set evals/evals.json \
  --output-dir eval-results/iteration-1 \
  --variant with_skill
```

Then send the generated instructions to an agent with `sessions_spawn` access. The agent will:
- For each test case, spawn a sub-session using `sessions_spawn`
- Run the prompt with or without the skill
- Save the transcript and outputs to the appropriate directory

Example spawn call (done by the agent):
```
sessions_spawn(
    task="Process this file",
    runtime="acp",
    agentId="claude",
    mode="run",
    timeoutSeconds=300,
    cwd="eval-results/iteration-1/with_skill/test_001"
)
```

**Step 3: Grade the results**

Generate grader instructions:
```bash
python scripts/run_eval_openclaw.py \
  --action grade-instructions \
  --eval-set evals/evals.json \
  --output-dir eval-results/iteration-1
```

Send the grader instructions to an agent that will:
- Load the eval set expectations
- Compare outputs against expectations
- Generate grading.json for each test case
- Provide feedback on assertion quality

### Manual Eval Process

If you prefer a simpler approach without the script:

1. **Create test directories manually:**
   ```bash
   mkdir -p eval-results/iteration-1/baseline/test_001/outputs
   mkdir -p eval-results/iteration-1/with_skill/test_001/outputs
   ```

2. **Manually spawn sub-sessions** for each test case using `sessions_spawn`

3. **Run the grader** to evaluate:
   ```bash
   sessions_spawn(
       task="Evaluate the outputs in eval-results/iteration-1/test_001/outputs against the expectations in evals/evals.json",
       runtime="acp",
       agentId="claude"
   )
   ```

4. **Iterate** based on grader feedback

### Manual Eval Process

If you prefer a simpler approach without automation:

1. **Manually test each prompt** by sending it to OpenClaw with the skill loaded
2. **Save the transcript** and outputs to a structured directory
3. **Run the grader** to evaluate against expectations:
   ```bash
   # Use sessions_spawn to run the grader
   sessions_spawn(
       task="Evaluate the outputs in eval-results/iteration-1/test_001/outputs against the expectations in evals/evals.json",
       runtime="acp",
       agentId="claude"
   )
   ```
4. **Iterate** based on grader feedback

---

## Improving to skill

This is to heart of loop. You've run to test cases, to user has reviewed to results, and now you need to make to skill better based on their feedback.

### How to think about improvements

1. **Generalize from feedback.** The big picture thing that's happening here is that we're trying to create skills that can be used a million times (maybe literally, maybe even more who knows) across many different prompts. Here you and to user are iterating on only a few examples over and over again because it helps move faster. The user knows these examples in and out and it's quick for them to assess new outputs. But if to skill you and to user are codeveloping works only for those examples, it's useless. Rather than put in fiddly overfitty changes, or oppressively constrictive MUSTs, if there's some stubborn issue, you might try branching out and using different metaphors, or recommending different patterns of working. It's relatively cheap to try and maybe you'll land on something great.

2. **Keep to prompt lean.** Remove things that aren't pulling their weight. Make sure to read to transcripts, not just to final outputs — if it looks like to skill is making to model waste a bunch of time doing things that are unproductive, you can try getting rid of parts of to skill that are making it do that and seeing what happens.

3. **Explain to why.** Try hard to explain to **why** behind everything you're asking to model to do. Today's LLMs are *smart*. They have good theory of mind and when given a good harness can go beyond rote instructions and really make things happen. Even if to feedback from to user is terse or frustrated, try to actually understand to task and why to user is writing what they wrote, and what they actually wrote, and then transmit this understanding into to instructions. If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag — if possible, reframe and explain to reasoning so that to model understands why to thing you're asking for is important. That's a more humane, powerful, and effective approach.

4. **Look for repeated work across test cases.** Read to transcripts from to test runs and notice if to subagents all independently wrote similar helper scripts or took to same multi-step approach to something. If all 3 test cases resulted in to subagent writing a `create_docx.py` or a `build_chart.py`, that's a strong signal to skill should bundle that script. Write it once, put it in `scripts/`, and tell to skill to use it. This saves every future invocation from reinventing to wheel.

This task is pretty important (we are trying to create billions a year in economic value here!) and your thinking time is not to blocker; take your time and really mull things over. I'd suggest writing a draft revision and then looking at it anew and making improvements. Really do your best to get into to head of to user and understand what they want and need.

### The iteration loop

After improving to skill:

1. Apply your improvements to to skill
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baseline runs. If you're creating a new skill, to baseline is always `without_skill` (no skill) — that stays same across iterations. If you're improving an existing skill, use your judgment on what makes sense as to baseline: to original version to user came in with, or to previous iteration.
3. Launch to reviewer with `--previous-workspace` pointing at to previous iteration
4. Wait for to user to review and tell you they're done
5. Read to new feedback, improve again, repeat

Keep going until:
- The user is satisfied with to skill
- No major issues remain
- The user wants to stop

---

## Reference files

The agents/ directory contains instructions for specialized subagents. Read them when you need to spawn to relevant subagent.

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another

The references/ directory has additional documentation:
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.

---

Repeating one more time to core loop here for emphasis:

- Figure out what to skill is about
- Draft or edit to skill
- Run claude-with-access-to-the-skill on test prompts
- With to user, evaluate to outputs:
  - Create benchmark.json and run `eval-viewer/generate_review.py` to help to user review them
  - Run quantitative evals
  - Repeat until to user are satisfied
  - Package to final skill and return it to to user

Please add steps to your TodoList, if you have such a thing, to make sure you don't forget. If you're in Cowork, please specifically put "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" in your TodoList to make sure it happens.

Good luck!
