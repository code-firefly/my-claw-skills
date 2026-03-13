#!/bin/bash

# 推送到 GitHub 脚本
# 使用方式：./push-to-github.sh

set -e

echo "🚀 开始推送到 GitHub..."
echo ""

# 检查当前目录
if [ ! -f "VERSION" ]; then
    echo "❌ 错误：当前目录不是 my-claw-skills 根目录"
    exit 1
fi

# 显示当前状态
echo "📋 当前状态："
git status --short
echo ""

# 推送到 GitHub
echo "📤 推送到 GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "🔗 仓库地址：https://github.com/code-firefly/my-claw-skills"
else
    echo ""
    echo "❌ 推送失败，请检查网络连接或认证信息"
    exit 1
fi
