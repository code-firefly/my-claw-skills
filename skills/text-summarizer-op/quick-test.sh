#!/bin/bash
# 快速测试脚本 - 手动运行一个测试用例

echo "=== Text Summarizer 技能快速测试 ==="
echo ""
echo "测试用例 1: 技术文档摘要"
echo "------------------------------------------------"
echo ""

# 创建一个临时测试目录
TEST_DIR="/tmp/text-summarizer-test"
mkdir -p "$TEST_DIR"

# 读取测试用例的 prompt
PROMPT=$(cat << 'EOF'
帮我总结一下这段技术文档：

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
EOF
)

echo "发送测试请求..."
echo "提示：请复制以下指令并发送给 OpenClaw agent："
echo ""
cat << 'PYTHON_CODE'
```python
# 使用 sessions_spawn 测试文本摘要技能
sessions_spawn(
    task="帮我总结一下这段技术文档：\n\n# REST API 设计指南\n\nRESTful API 是一种软件架构风格，用于设计网络应用程序。它基于 HTTP 协议，使用标准方法如 GET、POST、PUT、DELETE 来操作资源。\n\n## 核心原则\n\n1. **无状态性**：每个请求都包含所有必要信息\n2. **统一接口**：使用标准化的 URL 和方法\n3. **可缓存**：响应可以被缓存以提高性能\n4. **分层系统**：客户端不知道是否连接到终端服务器\n\n## 最佳实践\n\n- 使用名词而不是动词设计 URL（如 /users 而不是 /getUsers）\n- 使用 HTTP 状态码表示操作结果\n- 实现 CORS 以支持跨域请求\n- 使用 HTTPS 保证传输安全\n\n## 总结\n\n遵循 REST 原则可以创建可扩展、易维护的 API。",
    runtime="acp",
    agentId="claude",
    mode="run",
    timeoutSeconds=60,
    cwd="/tmp/text-summarizer-test"
)
```
PYTHON_CODE

echo ""
echo "================================================"
echo ""
echo "预期结果："
echo "- 摘要长度：3-5句话"
echo "- 包含核心原则：无状态性、统一接口、可缓存、分层系统"
echo "- 包含最佳实践：URL设计、状态码、CORS、HTTPS"
echo ""
echo "================================================"
echo ""
echo "测试脚本已准备完成！"
echo ""
echo "下一步操作："
echo "1. 在 OpenClaw 中复制上面的 sessions_spawn 调用"
echo "2. 等待结果返回"
echo "3. 检查输出是否符合预期"
echo ""
echo "完整评测示例请查看 README.md"
