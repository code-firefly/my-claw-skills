# my-claw-skills

> OpenClaw 专用技能集合 - 专业、高效、专注

## 📋 简介

这个仓库包含所有为 OpenClaw 平台开发的专用技能。每个技能都经过精心设计和优化，确保质量和用户体验。

## 🎯 技能列表

### [learn-system-openclaw](./learn-system-openclaw/) - 学习管理系统

完整的学习管理系统，支持：
- 🎯 学习目标管理（创建/追踪/切换/归档）
- 📚 课程管理（开始/完成/重置）
- 📊 进度追踪（总体/详细/自动计算）
- 🔖 书签系统（创建/继续/完成）
- 💾 知识缓存（初始化/刷新/查看）

**版本**: 1.0.0 | **状态**: ✅ 已完成，待测试

---

## 🚀 快速开始

### 安装技能

```bash
# 从 ClawHub 安装
clawhub install learn-system-openclaw

# 或从 GitHub 克隆仓库
git clone https://github.com/code-firefly/my-claw-skills.git
```

### 使用技能

```bash
# 在 OpenClaw 中使用
openclaw agent create learning-agent --skills learn-system-openclaw
openclaw session learning-agent
```

---

## 📖 开发指南

### 创建新技能

1. 创建技能目录
   ```bash
   mkdir my-new-skill
   cd my-new-skill
   ```

2. 创建必需文件
   - `SKILL.md` - 技能定义
   - `VERSION` - 版本号
   - `metadata.json` - 元数据

3. 提交并推送
   ```bash
   git add .
   git commit -m "feat: add my-new-skill"
   git push origin main
   ```

### 从 Universal Skills 转换

1. 参考 Universal 技能（`/home/wangxg/projects/my-skills/universal/`）
2. 转换为 OpenClaw 格式
3. 优化 description 和触发关键词
4. 测试验证
5. 发布到 ClawHub

---

## 🤝 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详情。

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

## 📞 联系方式

- **作者**: code-firefly
- **GitHub**: https://github.com/code-firefly/my-claw-skills
- **ClawHub**: (待发布）

---

## 🔗 相关仓库

- **Universal Skills**: https://github.com/code-firefly/my-skills
- **Claude Code Skills**: (待创建）

---

*Last Updated: 2026-03-13*
