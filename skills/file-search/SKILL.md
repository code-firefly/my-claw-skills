---
name: file-search
description: "使用 `fd` 和 `rg`（ripgrep）进行快速文件名和内容搜索。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["fd", "rg"] },
        "install":
          [
            {
              "id": "dnf-fd",
              "kind": "dnf",
              "package": "fd-find",
              "bins": ["fd"],
              "label": "安装 fd-find (dnf)",
            },
            {
              "id": "dnf-rg",
              "kind": "dnf",
              "package": "ripgrep",
              "bins": ["rg"],
              "label": "安装 ripgrep (dnf)",
            },
          ],
      },
  }
---

# 文件搜索技能 (File Search)

使用 `fd` 和 `rg`（ripgrep）进行快速文件名和内容搜索。

## 按名称查找文件

搜索匹配模式的文件：

```bash
fd "\.rs$" /home/xrx/projects
```

按精确名称查找文件：

```bash
fd -g "Cargo.toml" /home/xrx/projects
```

## 搜索文件内容

在文件中搜索正则表达式模式：

```bash
rg "TODO|FIXME" /home/xrx/projects
```

带上下文行的搜索：

```bash
rg -C 3 "fn main" /home/xrx/projects --type rust
```

## 安装

```bash
sudo dnf install fd-find ripgrep
```
