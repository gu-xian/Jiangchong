"""
论文处理API，支持降重和降低AI痕迹
"""
import json
import warnings

# 忽略所有警告
warnings.filterwarnings("ignore")

# 尝试导入jieba，如果不成功则使用简单替换
try:
    import jieba
    import re
    JIEBA_AVAILABLE = True
    
    # 简单的同义词词典
    SYNONYMS_DICT = {
        '使用': ['运用', '应用', '采用', '利用'],
        '研究': ['探讨', '分析', '探究', '研讨'],
        '问题': ['议题', '课题', '难题', '疑问'],
        '方法': ['方式', '途径', '手段', '办法'],
        '结果': ['成果', '结论', '效果', '成效'],
        '分析': ['探讨', '研究', '剖析', '解析'],
        '影响': ['作用', '效应', '冲击', '波及'],
        '发展': ['进展', '演变', '成长', '进步'],
        '提高': ['提升', '增强', '改善', '优化'],
        '实现': ['达成', '完成', '达到', '促成']
    }
    
    # AIGC降低痕迹用的转换规则
    AIGC_TRANSFORM_RULES = {
        '可以得出': '我觉得',
        '因此': '所以',
        '并且': '而且',
        '然而': '不过',
        '综上所述': '总的来说',
        '此外': '还有',
        '如果': '要是',
        '因为': '因为嘛',
        '所以': '所以啊',
        '但是': '但是呢',
        '例如': '比如说',
        '必须': '一定要',
        '需要': '得要'
    }
    
except ImportError:
    JIEBA_AVAILABLE = False


def process_text_with_jieba(text):
    """使用jieba处理降重文本"""
    try:
        # 分词
        words = jieba.lcut(text)
        result = []
        
        # 对每个词寻找同义词
        for word in words:
            # 跳过标点符号和空格
            if re.match(r'[\W\s]', word):
                result.append(word)
                continue
                
            # 在同义词词典中查找
            if word in SYNONYMS_DICT:
                # 使用第一个同义词替换
                result.append(SYNONYMS_DICT[word][0])
            else:
                result.append(word)
        
        return ''.join(result)
    except Exception as e:
        # 如果处理过程中出错，返回备用结果
        return text.replace("使用", "运用").replace("研究", "探讨")


def reduce_aigc_traces_with_jieba(text):
    """使用jieba处理降低AI痕迹的文本"""
    try:
        # 替换形式化表达为口语化表达
        result_text = text
        for formal, informal in AIGC_TRANSFORM_RULES.items():
            result_text = result_text.replace(formal, informal)
        
        return result_text
    except Exception as e:
        # 如果处理过程中出错，返回备用结果
        return text.replace("。", "。呢").replace("，", "，嗯")


def handler(request):
    """
    API处理函数
    """
    # 获取请求方法和路径
    method = request.get('method', '')
    path = request.get('path', '')
    
    # 处理健康检查
    if '/api/health' in path:
        return {
            'statusCode': 200,
            'body': json.dumps({
                "status": "ok", 
                "message": "API服务运行正常",
                "jieba_available": JIEBA_AVAILABLE
            }),
            'headers': {'Content-Type': 'application/json'}
        }
    
    # 处理文本处理API
    if '/api/process' in path and method == 'POST':
        try:
            # 解析请求体
            body_str = request.get('body', '{}')
            body = json.loads(body_str) if isinstance(body_str, str) else body_str
            
            text = body.get('text', '')
            mode = body.get('mode', 'reduce_weight')
            
            if not text:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': '请输入文本'}),
                    'headers': {'Content-Type': 'application/json'}
                }
            
            # 根据jieba是否可用选择处理方法
            if JIEBA_AVAILABLE:
                if mode == 'reduce_weight':
                    processed_text = process_text_with_jieba(text)
                else:
                    processed_text = reduce_aigc_traces_with_jieba(text)
            else:
                # 简单处理逻辑，不使用jieba
                if mode == 'reduce_weight':
                    processed_text = text.replace("使用", "运用").replace("研究", "探讨")
                else:
                    processed_text = text.replace("。", "。呢").replace("，", "，嗯")
            
            return {
                'statusCode': 200,
                'body': json.dumps({'result': processed_text}),
                'headers': {'Content-Type': 'application/json'}
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'服务器错误: {str(e)}'}),
                'headers': {'Content-Type': 'application/json'}
            }
    
    # 默认响应
    return {
        'statusCode': 404,
        'body': json.dumps({"error": "未找到该API端点"}),
        'headers': {'Content-Type': 'application/json'}
    } 