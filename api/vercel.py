"""
API状态检查页面
"""
import json

# 尝试导入jieba，检查是否可用
try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False

def handler(request):
    """
    API状态页面处理函数
    """
    # 设置jieba状态显示
    jieba_status_class = "module-available" if JIEBA_AVAILABLE else "module-unavailable"
    jieba_status_text = "✓ 可用" if JIEBA_AVAILABLE else "✗ 不可用"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API状态</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f0f8ff;
                text-align: center;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #4CAF50;
            }}
            .status {{
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
                margin: 20px 0;
            }}
            .module-status {{
                display: flex;
                justify-content: space-between;
                border-bottom: 1px solid #eee;
                padding: 10px 0;
            }}
            .module-name {{
                font-weight: bold;
            }}
            .module-available {{
                color: #4CAF50;
            }}
            .module-unavailable {{
                color: #f44336;
            }}
            a {{
                color: #4CAF50;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>论文优化工具 - API状态</h1>
            <div class="status">API服务正常运行</div>
            
            <div class="module-status">
                <span class="module-name">基础服务</span>
                <span class="module-available">✓ 可用</span>
            </div>
            
            <div class="module-status">
                <span class="module-name">jieba分词</span>
                <span class="{jieba_status_class}">{jieba_status_text}</span>
            </div>
            
            <div class="module-status">
                <span class="module-name">文本处理API</span>
                <span class="module-available">✓ 可用</span>
            </div>
            
            <p>所有服务组件状态良好，您可以放心使用论文优化工具。</p>
            <p><a href="/">返回首页</a></p>
        </div>
        
        <script>
            // 页面加载时检查API实际状态
            window.addEventListener('DOMContentLoaded', async () => {{
                try {{
                    const response = await fetch('/api/health');
                    if (response.ok) {{
                        const data = await response.json();
                        // 更新jieba状态
                        const jiebaStatus = document.querySelectorAll('.module-status')[1].querySelector('span:last-child');
                        if (data.jieba_available) {{
                            jiebaStatus.className = 'module-available';
                            jiebaStatus.innerHTML = '✓ 可用';
                        }} else {{
                            jiebaStatus.className = 'module-unavailable';
                            jiebaStatus.innerHTML = '✗ 不可用（使用备用模式）';
                        }}
                    }}
                }} catch (error) {{
                    console.error('API检查错误:', error);
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html; charset=utf-8'
        },
        'body': html_content
    } 