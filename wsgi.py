from app import app

# 这是Vercel需要的入口点
# Vercel会查找名为"app"的变量作为应用入口 

if __name__ == "__main__":
    app.run()

# Vercel处理函数
def handler(event, context):
    """
    Vercel Serverless Function处理程序
    """
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        },
        "body": "Flask应用正在运行"
    }
    
def start_response(status, headers):
    pass 