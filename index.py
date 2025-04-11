from app import app

# 这是Vercel Serverless Functions的入口点
def handler(request, **kwargs):
    """
    处理来自Vercel的请求
    """
    return app 