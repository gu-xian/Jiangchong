from flask import Flask, render_template, request, jsonify
import jieba
import re
import logging
import traceback
import os
from dotenv import load_dotenv
import random

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    # 形式化表达转口语化
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
    '需要': '得要',
    '认为': '我觉得',
    '表明': '说明',
    '显示': '看起来是',
    '证明': '表明',
    '建议': '我建议',
    '总结': '总而言之',
    '进行': '做',
    '当前': '现在'
}

def create_app():
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # 添加一个简单的健康检查路由
    @app.route('/_health')
    def health_check():
        return jsonify({"status": "ok"})
    
    def process_text(text):
        try:
            logger.info(f"开始处理降重文本，长度：{len(text)}")
            # 分词
            words = jieba.lcut(text)
            logger.debug(f"分词结果：{words}")
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
            
            final_text = ''.join(result)
            logger.info("降重文本处理完成")
            return final_text
        except Exception as e:
            logger.error(f"处理降重文本时出错: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def reduce_aigc_traces(text):
        try:
            logger.info(f"开始处理降AIGC文本，长度：{len(text)}")
            
            # 替换形式化表达为口语化表达
            result_text = text
            for formal, informal in AIGC_TRANSFORM_RULES.items():
                result_text = result_text.replace(formal, informal)
            
            # 增加一些语气词，使文本更自然
            sentences = re.split(r'([。！？])', result_text)
            result = []
            
            for i in range(0, len(sentences), 2):
                if i < len(sentences):
                    sentence = sentences[i]
                    if sentence and len(sentence) > 10 and random.random() < 0.3:
                        # 随机在句子中加入语气词
                        mood_words = ['嗯', '呢', '啊', '吧', '呀']
                        if random.random() < 0.5:
                            # 在句首加入语气词
                            sentence = random.choice(['其实', '说实话', '老实说', '坦白讲', '我认为']) + sentence
                        result.append(sentence)
                    else:
                        result.append(sentence)
                
                if i+1 < len(sentences):
                    result.append(sentences[i+1])  # 添加标点符号
            
            final_text = ''.join(result)
            logger.info("降AIGC文本处理完成")
            return final_text
        except Exception as e:
            logger.error(f"处理降AIGC文本时出错: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    @app.route('/')
    def home():
        try:
            logger.info("访问主页")
            return render_template('index.html')
        except Exception as e:
            logger.error(f"渲染主页时出错: {str(e)}")
            logger.error(traceback.format_exc())
            return "服务器错误，请稍后重试", 500

    @app.route('/process', methods=['POST'])
    def process():
        try:
            logger.info("收到处理请求")
            if not request.is_json:
                logger.error("请求格式错误：不是JSON格式")
                return jsonify({'error': '请求格式错误'}), 400

            text = request.json.get('text', '')
            mode = request.json.get('mode', 'reduce_weight')  # 默认为降重模式
            
            if not text:
                logger.error("请求错误：文本为空")
                return jsonify({'error': '请输入文本'}), 400
                
            logger.info(f"开始处理文本，模式: {mode}, 长度: {len(text)}")
            
            if mode == 'reduce_weight':
                processed_text = process_text(text)
            elif mode == 'reduce_aigc':
                processed_text = reduce_aigc_traces(text)
            else:
                logger.error(f"未知的处理模式: {mode}")
                return jsonify({'error': '未知的处理模式'}), 400
                
            return jsonify({'result': processed_text})
        except Exception as e:
            logger.error(f"处理请求时出错: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({'error': '服务器错误，请稍后重试'}), 500

    @app.errorhandler(404)
    def not_found(error):
        logger.error(f"404错误: {error}")
        return render_template('index.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"500错误: {error}")
        return "服务器错误，请稍后重试", 500

    return app

app = create_app()

if __name__ == '__main__':
    try:
        port = int(os.getenv('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"服务器启动失败: {str(e)}")
        logger.error(traceback.format_exc())
        print("\n服务器启动失败，请检查错误日志。")