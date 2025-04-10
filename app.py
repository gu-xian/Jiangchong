from flask import Flask, render_template, request, jsonify
import jieba
import re
import logging
import traceback
import os
from dotenv import load_dotenv

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

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

    def process_text(text):
        try:
            logger.info(f"开始处理文本，长度：{len(text)}")
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
            logger.info("文本处理完成")
            return final_text
        except Exception as e:
            logger.error(f"处理文本时出错: {str(e)}")
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
            if not text:
                logger.error("请求错误：文本为空")
                return jsonify({'error': '请输入文本'}), 400
                
            logger.info(f"开始处理文本，长度: {len(text)}")
            processed_text = process_text(text)
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
        input("按回车键退出...")