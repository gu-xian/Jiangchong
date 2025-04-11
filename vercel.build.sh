#!/bin/bash

# 输出调试信息
echo "开始Vercel构建脚本"

# 安装依赖
pip install -r requirements.txt

# 检查jieba库是否正确安装
echo "检查jieba库..."
python -c "import jieba; print('jieba版本:', jieba.__version__)"

# 设置环境变量
export PYTHONWARNINGS="ignore::SyntaxWarning"

# 输出构建完成信息
echo "Vercel构建脚本执行完成" 