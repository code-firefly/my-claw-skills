---
name: gh-issues
description: "自动获取 GitHub Issues，派生子代理实现修复并打开 PR，然后监控和处理 PR 的 review 评论。支持持续监控、并发修复、自动回应 review。适用于批量处理 issue、自动修复 bug、监控 PR 状态、处理代码审查评论等场景。Fetch GitHub issues, spawn sub-agents to implement fixes and open PRs, then monitor and address PR review comments. Usage: /gh-issues [owner/repo] [--label bug] [--limit 5] [--milestone v1.0] [--assignee @me] [--fork user/repo] [--watch] [--interval 5] [--reviews-only] [--cron] [--dry-run] [--model glm-5] [--notify-channel -1002381931352]"
user-invocable: true
metadata:
  { "openclaw": { "requires": { "bins": ["curl", "git", "gh"] }, "primaryEnv": "GH_TOKEN" } }
---

# gh-issues — 使用并行子代理自动修复 GitHub Issues (Auto-fix GitHub Issues with Parallel Sub-agents)

你是一个编排者（orchestrator）。严格按照以下 6 个阶段执行。不要跳过阶段。

重要 — 不依赖 `gh` CLI。此技能仅使用 curl + GitHub REST API。GH_TOKEN 环境变量已由 OpenClaw 注入。在所有 API 调用中将其作为 Bearer token 传递：

```
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" ...
```

---

## Phase 1 — 解析参数 (Parse Arguments)

解析 /gh-issues 后提供的参数字符串。

位置参数 (Positional)：

- owner/repo — 可选。这是从中获取 issues 的源仓库（source repo）。如果省略，从当前 git remote 检测：
  `git remote get-url origin`
  从 URL 中提取 owner/repo（处理 HTTPS 和 SSH 格式）。
  - HTTPS: https://github.com/owner/repo.git → owner/repo
  - SSH: git@github.com:owner/repo.git → owner/repo
    如果不在 git 仓库中或找不到 remote，停止并提示错误，要求用户指定 owner/repo。

标志（Flags - 全部可选）：
| 标志 (Flag) | 默认值 (Default) | 描述 (Description) |
|------|---------|-------------|
| --label | _(none)_ | 按标签过滤（如 bug、`enhancement`） |
| --limit | 10 | 每次轮询获取的最大 issues 数 |
| --milestone | _(none)_ | 按里程碑标题过滤 |
| --assignee | _(none)_ | 按分配者过滤（`@me` 表示自己） |
| --state | open | Issue 状态：open、closed、all |
| --fork | _(none)_ | 你的 fork（`user/repo`），用于推送分支和打开 PR。Issues 从源仓库获取；代码推送到 fork；PR 从 fork 打开到源仓库。 |
| --watch | false | 在每批之后继续轮询新的 issues 和 PR 评论 |
| --interval | 5 | 轮询之间的分钟数（仅与 `--watch` 一起使用） |
| --dry-run | false | 仅获取和显示 — 不派生子代理 |
| --yes | false | 跳过确认并自动处理所有过滤的 issues |
| --reviews-only | false | 跳过 issue 处理（阶段 2-5）。仅运行阶段 6 — 检查打开的 PR 的 review 评论并处理它们。 |
| --cron | false | Cron 安全模式：获取 issues 并派生子代理，不等待结果即退出。 |
| --model | _(none)_ | 用于子代理的模型（如 `glm-5`、`zai/glm-5`）。如果未指定，使用代理的默认模型。 |
| --notify-channel | _(none)_ | Telegram 频道 ID，用于发送最终 PR 摘要（如 -1002381931352）。仅发送带有 PR 链接的最终结果，不发送状态更新。 |

存储解析的值以供后续阶段使用。

派生值 (Derived values)：

- SOURCE_REPO = 位置参数 owner/repo（issues 所在位置）
- PUSH_REPO = 如果提供了 --fork 则使用该值，否则与 SOURCE_REPO 相同
- FORK_MODE = 如果提供了 --fork 则为 true，否则为 false

**如果设置了 `--reviews-only`**：直接跳到阶段 6。先运行 token 解析（来自阶段 2），然后跳到阶段 6。

**如果设置了 `--cron`**：

- 强制 `--yes`（跳过确认）
- 如果同时设置了 `--reviews-only`，运行 token 解析然后跳到阶段 6（cron review 模式）
- 否则，正常通过阶段 2-5，cron-mode 行为处于活动状态

---

## Phase 2 — 获取 Issues (Fetch Issues)

**Token 解析 (Token Resolution):**
首先，确保 GH_TOKEN 可用。检查环境：

```
echo $GH_TOKEN
```

如果为空，从配置读取：

```
cat ~/.openclaw/openclaw.json | jq -r '.skills.entries["gh-issues"].apiKey // empty'
```

如果仍然为空，检查 `/data/.clawdbot/openclaw.json`：

```
cat /data/.clawdbot/openclaw.json | jq -r '.skills.entries["gh-issues"].apiKey // empty'
```

导出为 GH_TOKEN 以供后续命令使用：

```
export GH_TOKEN="<token>"
```

通过 exec 构建并运行对 GitHub Issues API 的 curl 请求：

```
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/{SOURCE_REPO}/issues?per_page={limit}&state={state}&{query_params}"
```

其中 {query_params} 由以下内容构建：

- labels={label} 如果提供了 --label
- milestone={milestone} 如果提供了 --milestone（注意：API 期望里程碑 _number_，因此如果用户提供标题，首先通过 GET /repos/{SOURCE_REPO}/milestones 解析并按标题匹配）
- assignee={assignee} 如果提供了 --assignee（如果是 @me，首先通过 `GET /user` 解析你的用户名）

重要：GitHub Issues API 也会返回 pull requests。过滤掉它们 — 排除响应对象中存在 pull_request 键的任何项目。

如果在 watch 模式下：也过滤掉 PROCESSED_ISSUES 集合中已有 issue 编号的任何问题。

错误处理 (Error handling)：

- 如果 curl 返回 HTTP 401 或 403 → 停止并告诉用户：
  > "GitHub authentication failed. Please check your apiKey in OpenClaw dashboard or in ~/.openclaw/openclaw.json under skills.entries.gh-issues."
- 如果响应为空数组（过滤后）→ 报告"No issues found matching filters"并停止（如果在 watch 模式则循环返回）。
- 如果 curl 失败或返回任何其他错误 → 逐字报告错误并停止。

解析 JSON 响应。对于每个 issue，提取：number、title、body、labels（标签名称数组）、assignees、html_url。

---

## Phase 3 — 展示和确认 (Present & Confirm)

显示获取的 issues 的 markdown 表格：

| #   | 标题 (Title)                         | 标签 (Labels)        |
| --- | ----------------------------- | ------------- |
| 42  | Fix null pointer in parser    | bug, critical |
| 37  | Add retry logic for API calls | enhancement   |

如果 FORK_MODE 处于活动状态，还显示：

> "Fork mode: branches will be pushed to {PUSH_REPO}, PRs will target `{SOURCE_REPO}`"

如果 `--dry-run` 处于活动状态：

- 显示表格并停止。不继续到阶段 4。

如果 `--yes` 处于活动状态：

- 显示表格以供可见
- 自动处理所有列出的 issues 而无需询问确认
- 直接继续到阶段 4

否则：
要求用户确认要处理哪些 issues：

- "all" — 处理每个列出的 issue
- 逗号分隔的数字（如 `42, 37`）— 仅处理这些
- "cancel" — 完全中止

在继续之前等待用户响应。

Watch 模式说明：在第一次轮询时，总是与用户确认（除非设置了 --yes）。在后续轮询中，自动处理所有新 issues 而无需重新确认（用户已经选择加入）。仍然显示表格，以便他们可以看到正在处理的内容。

---

## Phase 4 — 预先检查 (Pre-flight Checks)

通过 exec 顺序运行这些检查：

1. **脏工作树检查 (Dirty working tree check):**

   ```
   git status --porcelain
   ```

   如果输出非空，警告用户：

   > "Working tree has uncommitted changes. Sub-agents will create branches from HEAD — uncommitted changes will NOT be included. Continue?"
   > 等待确认。如果拒绝，停止。

2. **记录基础分支 (Record base branch):**

   ```
   git rev-parse --abbrev-ref HEAD
   ```

   存储为 BASE_BRANCH。

3. **验证远程访问 (Verify remote access):**
   如果 FORK_MODE：
   - 验证 fork remote 存在。检查是否存在名为 `fork` 的 git remote：
     ```
     git remote get-url fork
     ```
     如果不存在，添加它：
     ```
     git remote add fork https://x-access-token:$GH_TOKEN@github.com/{PUSH_REPO}.git
     ```
   - 还要验证 origin（源仓库）可达：
     ```
     git ls-remote --exit-code origin HEAD
     ```

   如果不是 FORK_MODE：

   ```
   git ls-remote --exit-code origin HEAD
   ```

   如果失败，停止并提示："Cannot reach remote origin. Check your network and git config."

4. **验证 GH_TOKEN 有效性 (Verify GH_TOKEN validity):**

   ```
   curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $GH_TOKEN" https://api.github.com/user
   ```

   如果 HTTP 状态不是 200，停止并提示：

   > "GitHub authentication failed. Please check your apiKey in OpenClaw dashboard or in ~/.openclaw/openclaw.json under skills.entries.gh-issues."

5. **检查现有 PR (Check for existing PRs):**
   对于每个确认的 issue 编号 N，运行：

   ```
   curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
     "https://api.github.com/repos/{SOURCE_REPO}/pulls?head={PUSH_REPO_OWNER}:fix/issue-{N}&state=open&per_page=1"
   ```

   （其中 PUSH_REPO_OWNER 是 `PUSH_REPO` 的 owner 部分）
   如果响应数组非空，从处理列表中删除该 issue 并报告：

   > "Skipping #{N} — PR already exists: {html_url}"

   如果所有 issues 都被跳过，报告并停止（如果在 watch 模式则循环返回）。

6. **检查进行中的分支（尚未创建 PR = 子代理仍在工作）(Check for in-progress branches):**
   对于每个剩余的 issue 编号 N（尚未被上面的 PR 检查跳过），检查在 **push repo**（可能是 fork，不是 origin）上是否存在 `fix/issue-{N}` 分支：

   ```
   curl -s -o /dev/null -w "%{http_code}" \
     -H "Authorization: Bearer $GH_TOKEN" \
     "https://api.github.com/repos/{PUSH_REPO}/branches/fix/issue-{N}"
   ```

   如果 HTTP 200 → 分支存在于 push repo 上但在步骤 5 中未找到打开的 PR。跳过该 issue：

   > "Skipping #{N} — branch fix/issue-{N} exists on {PUSH_REPO}, fix likely in progress"

   此检查使用 GitHub API 而不是 `git ls-remote`，以便在 fork 模式下正确工作（分支被推送到 fork，而不是 origin）。

   如果在此检查后所有 issues 都被跳过，报告并停止（如果在 watch 模式则循环返回）。

7. **检查基于声明（claim）的进行中跟踪 (Check claim-based in-progress tracking):**
   这防止先前 cron 运行的子代理仍在工作但尚未推送分支或打开 PR 时的重复处理。

   读取声明文件（如果缺失则创建空 `{}`）：

   ```
   CLAIMS_FILE="/data/.clawdbot/gh-issues-claims.json"
   if [ ! -f "$CLAIMS_FILE" ]; then
     mkdir -p /data/.clawdbot
     echo '{}' > "$CLAIMS_FILE"
   fi
   ```

   解析声明文件。对于每个条目，检查声明时间戳是否早于 2 小时。如果是，删除它（已过期 — 子代理可能已完成或静默失败）。写回清理后的文件：

   ```
   CLAIMS=$(cat "$CLAIMS_FILE")
   CUTOFF=$(date -u -d '2 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-2H +%Y-%m-%dT%H:%M:%SZ)
   CLAIMS=$(echo "$CLAIMS" | jq --arg cutoff "$CUTOFF" 'to_entries | map(select(.value > $cutoff)) | from_entries')
   echo "$CLAIMS" > "$CLAIMS_FILE"
   ```

   对于每个剩余的 issue 编号 N（尚未被步骤 5 或 6 跳过），检查 `{SOURCE_REPO}#{N}` 是否作为键存在于声明文件中。

   如果已被声明且未过期 → 跳过：

   > "Skipping #{N} — sub-agent claimed this issue {minutes}m ago, still within timeout window"

   其中 `{minutes}` 是从声明时间戳到现在的计算结果。

   如果在此检查后所有 issues 都被跳过，报告并停止（如果在 watch 模式则循环返回）。

---

## Phase 5 — 派生子代理（并行）(Spawn Sub-agents - Parallel)

**Cron 模式（`--cron` 处于活动状态）:**

- **顺序光标跟踪 (Sequential cursor tracking):** 使用光标文件跟踪下一个要处理的 issue：

  ```
  CURSOR_FILE="/data/.clawdbot/gh-issues-cursor-{SOURCE_REPO_SLUG}.json"
  # SOURCE_REPO_SLUG = owner-repo，斜杠替换为连字符（如 openclaw-openclaw）
  ```

  读取光标文件（如果缺失则创建）：

  ```
  if [ ! -f "$CURSOR_FILE" ]; then
    echo '{"last_processed": null, "in_progress": null}' > "$CURSOR_FILE"
  fi
  ```

  - `last_processed`: 最后完成的 issue 的编号（如果没有则为 null）
  - `in_progress`: 当前正在处理的 issue 编号（或 null）

- **选择下一个 issue (Select next issue):** 过滤获取的 issues 列表，找到第一个满足以下条件的 issue：
  - Issue 编号 > last_processed（如果设置了 last_processed）
  - 并且 issue 不在声明文件中（尚未在进行中）
  - 并且 issue 不存在 PR（在阶段 4 步骤 5 中检查）
  - 并且 push repo 上不存在分支（在阶段 4 步骤 6 中检查）
- 如果在 last_processed 光标之后未找到符合条件的 issue，则绕回到开头（从最早符合条件的 issue 开始）。

- 如果找到符合条件的 issue：
  1. 在光标文件中将其标记为 in_progress
  2. 为该 issue 派生单个子代理，使用 `cleanup: "keep"` 和 `runTimeoutSeconds: 3600`
  3. 如果提供了 `--model`，在 spawn 配置中包含 `model: "{MODEL}"`
  4. 如果提供了 `--notify-channel`，在任务中包含 channel，以便子代理可以通知
  5. 不要等待子代理结果 — 即发即忘
  6. **写入声明 (Write claim):** 派生后，读取声明文件，添加 `{SOURCE_REPO}#{N}` 并附带当前 ISO 时间戳，写回
  7. 立即报告："Spawned fix agent for #{N} — will create PR when complete"
  8. 退出技能。不要继续到结果收集或阶段 6。

- 如果未找到符合条件的 issue（所有 issues 都有 PR、分支或在进行中），报告"No eligible issues to process — all issues have PRs/branches or are in progress"并退出。

**普通模式（`--cron` 未处于活动状态）:**
对于每个确认的 issue，使用 sessions_spawn 派生子代理。最多同时启动 8 个（匹配 `subagents.maxConcurrent: 8`）。如果超过 8 个 issues，分批处理 — 每个完成时启动下一个代理。

**写入声明 (Write claims):** 派生每个子代理后，读取声明文件，添加 `{SOURCE_REPO}#{N}` 并附带当前 ISO 时间戳，写回（与 cron 模式相同的过程）。这涵盖了 watch 模式可能与 cron 运行重叠的交互使用。

### 子代理任务提示 (Sub-agent Task Prompt)

对于每个 issue，构建以下提示并通过 sessions_spawn 传递。要注入到模板的变量：

- {SOURCE_REPO} — issue 所在的上游仓库
- {PUSH_REPO} — 要推送分支的仓库（与 SOURCE_REPO 相同，除非在 fork 模式）
- {FORK_MODE} — true/false
- {PUSH_REMOTE} — 如果 FORK_MODE 则为 `fork`，否则为 `origin`
- {number}, {title}, {url}, {labels}, {body} — 来自 issue
- {BASE_BRANCH} — 来自阶段 4
- {notify_channel} — 用于通知的 Telegram 频道 ID（如果未设置则为空）。在下面的模板中用 `--notify-channel` 标志的值替换 {notify_channel}（如果未提供则保留为空字符串）。

构造任务时，包括 {notify_channel} 在内的所有模板变量都用实际值替换。

```
You are a focused code-fix agent. Your task is to fix a single GitHub issue and open a PR.

IMPORTANT: Do NOT use the gh CLI — it is not installed. Use curl with the GitHub REST API for all GitHub operations.

First, ensure GH_TOKEN is set. Check: `echo $GH_TOKEN`. If empty, read from config:
GH_TOKEN=$(cat ~/.openclaw/openclaw.json 2>/dev/null | jq -r '.skills.entries["gh-issues"].apiKey // empty') || GH_TOKEN=$(cat /data/.clawdbot/openclaw.json 2>/dev/null | jq -r '.skills.entries["gh-issues"].apiKey // empty')

Use the token in all GitHub API calls:
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" ...

<config>
Source repo (issues): {SOURCE_REPO}
Push repo (branches + PRs): {PUSH_REPO}
Fork mode: {FORK_MODE}
Push remote name: {PUSH_REMOTE}
Base branch: {BASE_BRANCH}
Notify channel: {notify_channel}
</config>

<issue>
Repository: {SOURCE_REPO}
Issue: #{number}
Title: {title}
URL: {url}
Labels: {labels}
Body: {body}
</issue>

<instructions>
Follow these steps in order. If any step fails, report the failure and stop.

0. SETUP — Ensure GH_TOKEN is available:
```

export GH_TOKEN=$(node -e "const fs=require('fs'); const c=JSON.parse(fs.readFileSync('/data/.clawdbot/openclaw.json','utf8')); console.log(c.skills?.entries?.['gh-issues']?.apiKey || '')")

```
If that fails, also try:
```

export GH_TOKEN=$(cat ~/.openclaw/openclaw.json 2>/dev/null | node -e "const fs=require('fs');const d=JSON.parse(fs.readFileSync(0,'utf8'));console.log(d.skills?.entries?.['gh-issues']?.apiKey||'')")

```
Verify: echo "Token: ${GH_TOKEN:0:10}..."

1. CONFIDENCE CHECK — Before implementing, assess whether this issue is actionable:
- Read the issue body carefully. Is the problem clearly described?
- Search the codebase (grep/find) for relevant code. Can you locate it?
- Is the scope reasonable? (single file/function = good, whole subsystem = bad)
- Is a specific fix suggested or is it a vague complaint?

Rate your confidence (1-10). If confidence < 7, STOP and report:
> "Skipping #{number}: Low confidence (score: N/10) — [reason: vague requirements | cannot locate code | scope too large | no clear fix suggested]"

Only proceed if confidence >= 7.

1. UNDERSTAND — Read the issue carefully. Identify what needs to change and where.

2. BRANCH — Create a feature branch from the base branch:
git checkout -b fix/issue-{number} {BASE_BRANCH}

3. ANALYZE — Search the codebase to find relevant files:
- Use grep/find via exec to locate code related to the issue
- Read relevant files to understand current behavior
- Identify the root cause

4. IMPLEMENT — Make a minimal, focused fix:
- Follow existing code style and conventions
- Change only what is necessary to fix the issue
- Do not add unrelated changes or new dependencies without justification

5. TEST — Discover and run the existing test suite if one exists:
- Look for package.json scripts, Makefile targets, pytest, cargo test, etc.
- Run relevant tests
- If tests fail after your fix, attempt ONE retry with a corrected approach
- If tests still fail, report the failure

6. COMMIT — Stage and commit your changes:
git add {changed_files}
git commit -m "fix: {short_description}

Fixes {SOURCE_REPO}#{number}"

7. PUSH — Push the branch:
First, ensure the push remote uses token auth and disables credential helpers:
git config --global credential.helper ""
git remote set-url {PUSH_REMOTE} https://x-access-token:$GH_TOKEN@github.com/{PUSH_REPO}.git
Then push:
GIT_ASKPASS=true git push -u {PUSH_REMOTE} fix/issue-{number}

8. PR — Create a pull request using the GitHub API:

If FORK_MODE is true, the PR goes from your fork to the source repo:
- head = "{PUSH_REPO_OWNER}:fix/issue-{number}"
- base = "{BASE_BRANCH}"
- PR is created on {SOURCE_REPO}

If FORK_MODE is false:
- head = "fix/issue-{number}"
- base = "{BASE_BRANCH}"
- PR is created on {SOURCE_REPO}

curl -s -X POST \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/{SOURCE_REPO}/pulls \
  -d '{
    "title": "fix: {title}",
    "head": "{head_value}",
    "base": "{BASE_BRANCH}",
    "body": "## Summary\n\n{one_paragraph_description_of_fix}\n\n## Changes\n\n{bullet_list_of_changes}\n\n## Testing\n\n{what_was_tested_and_results}\n\nFixes {SOURCE_REPO}#{number}"
  }'

Extract the `html_url` from the response — this is the PR link.

9. REPORT — Send back a summary:
- PR URL (the html_url from step 8)
- Files changed (list)
- Fix summary (1-2 sentences)
- Any caveats or concerns

10. NOTIFY (if notify_channel is set) — If {notify_channel} is not empty, send a notification to the Telegram channel:
```

Use the message tool with:

- action: "send"
- channel: "telegram"
- target: "{notify_channel}"
- message: "✅ PR Created: {SOURCE_REPO}#{number}

{title}

{pr_url}

Files changed: {files_changed_list}"

```
</instructions>

<constraints>
- No force-push, no modifying the base branch
- No unrelated changes or gratuitous refactoring
- No new dependencies without strong justification
- If the issue is unclear or too complex to fix confidently, report your analysis instead of guessing
- Do NOT use the gh CLI — it is not available. Use curl + the GitHub REST API for all GitHub operations.
- GH_TOKEN is already in the environment — do NOT prompt for auth
- Time limit: you have 60 minutes max. Be thorough — analyze properly, test your fix, don't rush.
</constraints>
```

### 每个子代理的 Spawn 配置 (Spawn configuration per sub-agent):

- runTimeoutSeconds: 3600（60 分钟）
- cleanup: "keep"（保留转录以供审查）
- 如果提供了 `--model`，在 spawn 配置中包含 `model: "{MODEL}"`

### 超时处理 (Timeout Handling)

如果子代理超过 60 分钟，记录为：

> "#{N} — Timed out (issue may be too complex for auto-fix)"

---

## 结果收集 (Results Collection)

**如果 `--cron` 处于活动状态：** 完全跳过此部分 — 编排者已在阶段 5 派生后退出。

在所有子代理完成（或超时）后，收集它们的结果。将成功打开的 PR 列表存储在 `OPEN_PRS` 中（PR 编号、分支名称、issue 编号、PR URL）以供阶段 6 使用。

显示摘要表格：

| Issue                 | 状态 (Status)    | PR                             | 备注 (Notes)                          |
| --------------------- | --------- | ------------------------------ | ------------------------------ |
| #42 Fix null pointer  | PR opened | https://github.com/.../pull/99 | 3 files changed                |
| #37 Add retry logic   | Failed    | --                             | Could not identify target code |
| #15 Update docs       | Timed out | --                             | Too complex for auto-fix       |
| #8 Fix race condition | Skipped   | --                             | PR already exists              |

**状态值 (Status values):**

- **PR opened** — 成功，链接到 PR
- **Failed** — 子代理无法完成（在备注中包含原因）
- **Timed out** — 超过 60 分钟限制
- **Skipped** — 在预先检查中检测到现有 PR

以一行摘要结束：

> "Processed {N} issues: {success} PRs opened, {failed} failed, {skipped} skipped."

**发送通知到频道（如果设置了 --notify-channel）:**
如果提供了 `--notify-channel`，使用 `message` 工具将最终摘要发送到该 Telegram 频道：

```
使用 message 工具：
- action: "send"
- channel: "telegram"
- target: "{notify-channel}"
- message: "✅ GitHub Issues Processed

Processed {N} issues: {success} PRs opened, {failed} failed, {skipped} skipped.

{PR_LIST}"

其中 PR_LIST 仅包括成功打开的 PR，格式为：
• #{issue_number}: {PR_url} ({notes})
```

然后继续到阶段 6。

---

## Phase 6 — PR 审查处理器 (PR Review Handler)

此阶段监控打开的 PR（由此技能创建或预先存在的 `fix/issue-*` PR）的 review 评论，并派生子代理来处理它们。

**此阶段何时运行 (When this phase runs):**

- 结果收集之后（阶段 2-5 完成）— 检查刚刚打开的 PR
- 当设置 `--reviews-only` 标志时 — 完全跳过阶段 2-5，仅运行此阶段
- 在 watch 模式下 — 每次轮询周期后运行，在检查新的 issues 之后

**Cron review 模式（`--cron --reviews-only`）:**
当同时设置 `--cron` 和 `--reviews-only` 时：

1. 运行 token 解析（阶段 2 token 部分）
2. 发现打开的 `fix/issue-*` PR（步骤 6.1）
3. 获取 review 评论（步骤 6.2）
4. **分析评论内容的可操作性**（步骤 6.3）
5. 如果发现可操作的评论，为第一个带有未处理评论的 PR 派生 ONE review-fix 子代理 — 即发即忘（不要等待结果）
   - 使用 `cleanup: "keep"` 和 `runTimeoutSeconds: 3600`
   - 如果提供了 `--model`，在 spawn 配置中包含 `model: "{MODEL}"`
6. 报告："Spawned review handler for PR #{N} — will push fixes when complete"
7. 立即退出技能。不要继续到步骤 6.5（Review Results）。

如果未发现可操作的评论，报告"No actionable review comments found"并退出。

**普通模式（非 cron）继续如下：**

### 步骤 6.1 — 发现要监控的 PR (Discover PRs to Monitor)

收集要检查 review 评论的 PR：

**如果来自阶段 5：** 使用结果收集中的 `OPEN_PRS` 列表。

**如果是 `--reviews-only` 或后续 watch 循环：** 获取所有带有 `fix/issue-` 分支模式的打开 PR：

```
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/{SOURCE_REPO}/pulls?state=open&per_page=100"
```

过滤到仅 `head.ref` 以 `fix/issue-` 开头的 PR。

对于每个 PR，提取：`number`（PR 编号）、`head.ref`（分支名称）、`html_url`、`title`、`body`。

如果未找到 PR，报告"No open fix/ PRs to monitor"并停止（如果在 watch 模式则循环返回）。

### 步骤 6.2 — 获取所有审查源 (Fetch All Review Sources)

对于每个 PR，从多个源获取 reviews：

**获取 PR reviews：**

```
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/{SOURCE_REPO}/pulls/{pr_number}/reviews"
```

**获取 PR review 评论（内联/文件级别）：**

```
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/{SOURCE_REPO}/pulls/{pr_number}/comments"
```

**获取 PR issue 评论（一般对话）：**

```
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/{SOURCE_REPO}/issues/{pr_number}/comments"
```

**获取 PR body 以获取嵌入的 reviews：**
一些 review 工具（如 Greptile）直接在 PR body 中嵌入它们的反馈。检查：

- `<!-- greptile_comment -->` 标记
- PR body 中的其他结构化 review 部分

```
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/{SOURCE_REPO}/pulls/{pr_number}"
```

提取 `body` 字段并解析嵌入的 review 内容。

### 步骤 6.3 — 分析评论的可操作性 (Analyze Comments for Actionability)

**确定 bot 自己的用户名**以进行过滤：

```
curl -s -H "Authorization: Bearer $GH_TOKEN" https://api.github.com/user | jq -r '.login'
```

存储为 `BOT_USERNAME`。排除任何 `user.login` 等于 `BOT_USERNAME` 的评论。

**对于每个评论/review，分析内容以确定是否需要操作：**

**不可操作（跳过）(NOT actionable - skip):**

- 纯批准或"LGTM"而没有建议
- 仅信息性的 bot 评论（CI 状态、没有特定请求的自动生成摘要）
- 已被处理的评论（检查 bot 是否回复了"Addressed in commit..."）
- 状态为 `APPROVED` 且没有请求更改的内联评论的 reviews

**可操作（需要关注）(IS actionable - requires attention):**

- 状态为 `CHANGES_REQUESTED` 的 reviews
- 状态为 `COMMENTED` 并包含特定请求的 reviews：
  - "this test needs to be updated"
  - "please fix"、"change this"、"update"、"can you"、"should be"、"needs to"
  - "will fail"、"will break"、"causes an error"
  - 提及特定代码问题（bug、缺少错误处理、边缘情况）
- 指出代码中问题的内联 review 评论
- PR body 中的嵌入 reviews，识别：
  - 关键问题或破坏性更改
  - 预期的测试失败
  - 需要关注的特定代码
  - 有担忧的置信度分数

**解析嵌入的 review 内容（如 Greptile）(Parse embedded review content):**
查找用 `<!-- greptile_comment -->` 或类似标记的部分。提取：

- 摘要文本
- 任何提及"Critical issue"、"needs attention"、"will fail"、"test needs to be updated"
- 低于 4/5 的置信度分数（表示担忧）

**构建 actionable_comments 列表 (Build actionable_comments list)**，包括：

- 源（review、内联评论、PR body 等）
- 作者
- 正文文本
- 对于内联：文件路径和行号
- 识别的特定操作项

如果在任何 PR 中未发现可操作的评论，报告"No actionable review comments found"并停止（如果在 watch 模式则循环返回）。

### 步骤 6.4 — 展示审查评论 (Present Review Comments)

显示带有待处理可操作评论的 PR 表格：

```
| PR | 分支 (Branch) | 可操作评论 (Actionable Comments) | 来源 (Sources) |
|----|--------|---------------------|---------|
| #99 | fix/issue-42 | 2 comments | @reviewer1, greptile |
| #101 | fix/issue-37 | 1 comment | @reviewer2 |
```

如果未设置 `--yes` 并且这不是后续的 watch 轮询：要求用户确认要处理哪些 PR（"all"、逗号分隔的 PR 编号或"skip"）。

### 步骤 6.5 — 派生 Review 修复子代理（并行）(Spawn Review Fix Sub-agents - Parallel)

对于每个带有可操作评论的 PR，派生子代理。最多同时启动 8 个。

**Review 修复子代理提示 (Review fix sub-agent prompt):**

```
You are a PR review handler agent. Your task is to address review comments on a pull request by making the requested changes, pushing updates, and replying to each comment.

IMPORTANT: Do NOT use the gh CLI — it is not installed. Use curl with the GitHub REST API for all GitHub operations.

First, ensure GH_TOKEN is set. Check: echo $GH_TOKEN. If empty, read from config:
GH_TOKEN=$(cat ~/.openclaw/openclaw.json 2>/dev/null | jq -r '.skills.entries["gh-issues"].apiKey // empty') || GH_TOKEN=$(cat /data/.clawdbot/openclaw.json 2>/dev/null | jq -r '.skills.entries["gh-issues"].apiKey // empty')

<config>
Repository: {SOURCE_REPO}
Push repo: {PUSH_REPO}
Fork mode: {FORK_MODE}
Push remote: {PUSH_REMOTE}
PR number: {pr_number}
PR URL: {pr_url}
Branch: {branch_name}
</config>

<review_comments>
{json_array_of_actionable_comments}

Each comment has:
- id: comment ID（用于回复）
- user: 谁留下的它
- body: 评论文本
- path: 文件路径（对于内联评论）
- line: 行号（对于内联评论）
- diff_hunk: 周围 diff 上下文（对于内联评论）
- source: 评论来自哪里（review、inline、pr_body、greptile 等）
</review_comments>

<instructions>
Follow these steps in order:

0. SETUP — Ensure GH_TOKEN is available:
```

export GH_TOKEN=$(node -e "const fs=require('fs'); const c=JSON.parse(fs.readFileSync('/data/.clawdbot/openclaw.json','utf8')); console.log(c.skills?.entries?.['gh-issues']?.apiKey || '')")

```
Verify: echo "Token: ${GH_TOKEN:0:10}..."

1. CHECKOUT — Switch to the PR branch:
git fetch {PUSH_REMOTE} {branch_name}
git checkout {branch_name}
git pull {PUSH_REMOTE} {branch_name}

2. UNDERSTAND — Read ALL review comments carefully. Group them by file. Understand what each reviewer is asking for.

3. IMPLEMENT — For each comment, make the requested change:
- Read the file and locate the relevant code
- Make the change the reviewer requested
- If the comment is vague or you disagree, still attempt a reasonable fix but note your concern
- If the comment asks for something impossible or contradictory, skip it and explain why in your reply

4. TEST — Run existing tests to make sure your changes don't break anything:
- If tests fail, fix the issue or revert the problematic change
- Note any test failures in your replies

5. COMMIT — Stage and commit all changes in a single commit:
git add {changed_files}
git commit -m "fix: address review comments on PR #{pr_number}

Addresses review feedback from {reviewer_names}"

6. PUSH — Push the updated branch:
git config --global credential.helper ""
git remote set-url {PUSH_REMOTE} https://x-access-token:$GH_TOKEN@github.com/{PUSH_REPO}.git
GIT_ASKPASS=true git push {PUSH_REMOTE} {branch_name}

7. REPLY — For each addressed comment, post a reply:

对于内联 review 评论（有路径/行），回复评论线程：
curl -s -X POST \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/{SOURCE_REPO}/pulls/{pr_number}/comments/{comment_id}/replies \
  -d '{"body": "Addressed in commit {short_sha} — {brief_description_of_change}"}'

对于一般 PR 评论（issue 评论），在 PR 上回复：
curl -s -X POST \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/{SOURCE_REPO}/issues/{pr_number}/comments \
  -d '{"body": "Addressed feedback from @{reviewer}:\n\n{summary_of_changes_made}\n\nUpdated in commit {short_sha}"}'

对于你无法处理的评论，回复解释原因：
"Unable to address this comment: {reason}. This may need manual review."

8. REPORT — Send back a summary:
- PR URL
- 已处理与跳过的评论数量
- Commit SHA
- 更改的文件
- 需要手动关注的任何评论
</instructions>

<constraints>
- 仅修改与 review 评论相关的文件
- 不要进行无关的更改
- 不要 force-push — 始终常规推送
- 如果评论与另一个评论矛盾，处理最新的一个并标记冲突
- 不要使用 gh CLI — 使用 curl + GitHub REST API
- GH_TOKEN 已在环境中 — 不要提示认证
- 时间限制：最多 60 分钟
</constraints>
```

**每个子代理的 Spawn 配置 (Spawn configuration per sub-agent):**

- runTimeoutSeconds: 3600（60 分钟）
- cleanup: "keep"（保留转录以供审查）
- 如果提供了 `--model`，在 spawn 配置中包含 `model: "{MODEL}"`

### 步骤 6.6 — 审查结果 (Review Results)

所有 review 子代理完成后，显示摘要：

```
| PR | 已处理评论 (Comments Addressed) | 跳过评论 (Comments Skipped) | 提交 (Commit) | 状态 (Status) |
|----|-------------------|-----------------|--------|--------|
| #99 fix/issue-42 | 3 | 0 | abc123f | All addressed |
| #101 fix/issue-37 | 1 | 1 | def456a | 1 needs manual review |
```

将此批次的评论 ID 添加到 `ADDRESSED_COMMENTS` 集合以防止重新处理。

---

## Watch 模式（如果 --watch 处于活动状态）(Watch Mode - if --watch is active)

在展示当前批次的结果后：

1. 将此批次的所有 issue 编号添加到运行中的 PROCESSED_ISSUES 集合。
2. 将所有已处理的评论 ID 添加到 ADDRESSED_COMMENTS。
3. 告诉用户：
   > "Next poll in {interval} minutes... (say 'stop' to end watch mode)"
4. 休眠 {interval} 分钟。
5. 返回到 **阶段 2 — 获取 Issues**。获取将自动过滤掉：
   - 已经在 PROCESSED_ISSUES 中的 issues
   - 具有现有 fix/issue-{N} PR 的 issues（在阶段 4 预先检查中捕获）
6. 阶段 2-5 之后（或如果没有新 issues），运行 **阶段 6** 以检查所有跟踪 PR（新创建和先前打开的）上的新 review 评论。
7. 如果没有新 issues 并且没有新的可操作 review 评论 → 报告"No new activity. Polling again in {interval} minutes..."并循环回到步骤 4。
8. 用户可以随时说"stop"以退出 watch 模式。停止时，显示所有批次的最终累积摘要 — 已处理的 issues 和已处理的 review 评论。

**轮询之间的上下文卫生 — 重要 (Context hygiene between polls - IMPORTANT):**
仅在轮询周期之间保留：

- PROCESSED_ISSUES（issue 编号集合）
- ADDRESSED_COMMENTS（评论 ID 集合）
- OPEN_PRS（跟踪 PR 列表：编号、分支、URL）
- 累积结果（每个 issue 一行 + 每个 review 批次一行）
- 从阶段 1 解析的参数
- BASE_BRANCH、SOURCE_REPO、PUSH_REPO、FORK_MODE、BOT_USERNAME
  不要在轮询之间保留 issue bodies、评论 bodies、子代理转录或代码库分析。
