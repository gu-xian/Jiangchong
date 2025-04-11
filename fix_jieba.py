import re
import jieba
import sys

def fix_jieba_regex():
    """
    修复jieba库中的无效正则表达式转义序列
    """
    # 修复re_han_default正则表达式
    if hasattr(jieba, 're_han_default'):
        # 原始有问题的正则：([\u4E00-\u9FD5a-zA-Z0-9+#&\._%\-]+)
        # 修复后的正则：([\u4E00-\u9FD5a-zA-Z0-9+#&._%\-]+)
        pattern = r"([\u4E00-\u9FD5a-zA-Z0-9+#&._%\-]+)"
        jieba.re_han_default = re.compile(pattern, re.U)
        
    # 修复任何其他可能有类似问题的正则表达式
    # ...
    
    print("已修复jieba库的正则表达式问题", file=sys.stderr)

# 在导入jieba后立即应用修复
fix_jieba_regex() 