"""
论文优化工具API入口点
"""

def handler(request):
    """
    简单的入口点函数，返回HTML内容
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>论文优化工具</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f0f8ff;
                text-align: center;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #4CAF50;
            }
            .btn {
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 4px;
                text-decoration: none;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>论文优化工具</h1>
            <p>欢迎使用在线论文优化工具，支持论文降重和AI生成内容优化。</p>
            <p>目前API服务正在运行中！</p>
            <div>
                <a href="/static/index.html" class="btn">前往使用工具</a>
                <a href="/api/status" class="btn">检查API状态</a>
            </div>
            <p style="margin-top: 20px; font-size: 14px; color: #666;">
                © 2023 论文优化工具 - 仅供学习参考使用
            </p>
        </div>
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