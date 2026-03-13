# 贡献指南 (Contributing Guide)

感谢你对 my-claw-skills 项目的关注！我们欢迎任何形式的贡献。

---

## 🤝 如何贡献

### 报告 Bug

如果你发现了 bug，请：

1. 检查 [Issues](https://github.com/code-firefly/my-claw-skills/issues) 确认该问题未被报告
2. 创建新的 Issue，包含：
   - 清晰的标题
   - 复现步骤
   - 预期行为
   - 实际行为
   - 环境信息（OpenClaw 版本、操作系统等）

### 提出新功能

如果你有新功能的想法：

1. 先检查 [Issues](https://github.com/code-firefly/my-claw-skills/issues) 确认该功能未被提出
2. 创建新的 Issue，描述你的想法和使用场景
3. 等待维护者反馈和讨论

### 提交代码

如果你想要直接贡献代码：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📝 开发规范

### 代码风格

- 使用中文注释和文档
- 遵循现有的文件命名规范
- 保持代码简洁和可读性

### 提交信息规范

使用清晰的提交信息：

```
<type>: <subject>

<body>

<footer>
```

类型（type）：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 添加测试
- `chore`: 构建/工具链更新

示例：

```
feat: 添加书签系统

- 支持创建书签
- 支持继续书签探索
- 支持完成书签返回主线

Closes #123
```

### Pull Request 规范

PR 标题格式：

```
<type>: <subject>
```

PR 描述应包含：
- 改动说明
- 相关 Issue
- 测试说明
- 截图（如适用）

---

## 🧪 测试

在提交代码前，请确保：

1. 按照测试计划 (`TEST_PLAN.md`) 进行测试
2. 所有现有功能仍然正常工作
3. 新功能有相应的测试

---

## 📋 发布流程

版本发布遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)。

### 版本号格式

`MAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

### 发布步骤

1. 更新 `VERSION` 文件
2. 更新 `CHANGELOG.md`
3. 更新 `metadata.json` 中的版本号
4. 提交更改 (`git commit -m "chore: release v1.0.0"`)
5. 创建 Git tag (`git tag v1.0.0`)
6. 推送 tag (`git push origin v1.0.0`)
7. GitHub Actions 会自动发布到 ClawHub

---

## 📄 许可证

通过贡献代码，你同意你的贡献将在 MIT 许可证下发布。

---

## 📞 联系方式

- **作者**: code-firefly
- **GitHub**: https://github.com/code-firefly/my-claw-skills
- **ClawHub**: (待发布)

---

感谢你的贡献！🎉
