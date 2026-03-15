---
name: github
description: "使用 gh CLI 与 GitHub 交互。支持管理 issue、PR、CI 工作流，以及高级 API 查询。适用于创建 issue、查看 PR 状态、检查 CI 运行结果、查询仓库信息等场景。Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries."
---

# GitHub 技能 (GitHub Skill)

使用 `gh` CLI 与 GitHub 交互。当不在 git 目录中时，总是指定 `--repo owner/repo`，或直接使用 URL。

## 拉取请求 (Pull Requests)

检查 PR 的 CI 状态：
```bash
gh pr checks 55 --repo owner/repo
```

列出最近的工作流运行：
```bash
gh run list --repo owner/repo --limit 10
```

查看运行并查看哪些步骤失败：
```bash
gh run view <run-id> --repo owner/repo
```

仅查看失败步骤的日志：
```bash
gh run view <run-id> --repo owner/repo --log-failed
```

## 高级查询 API (API for Advanced Queries)

`gh api` 命令对于访问其他子命令不可用的数据很有用。

获取特定字段的 PR：
```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

## JSON 输出 (JSON Output)

大多数命令支持 `--json` 以进行结构化输出。你可以使用 `--jq` 进行过滤：

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```
