# Test 1: Technical Documentation Summary

**Date**: 2026-03-14
**Test ID**: 1
**Variant**: with_skill
**Skill**: text-summarizer-op

---

## User Prompt

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

---

## Expected Output

包含核心原则（无状态性、统一接口、可缓存、分层系统）和最佳实践（URL设计、状态码、CORS、HTTPS）的摘要，长度3-5句话

---

## Running test...

*Test will be executed below*
