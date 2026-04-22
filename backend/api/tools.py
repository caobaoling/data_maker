# 文件: api/tools.py
# 作者: Claude Code
# 创建日期: 2026/04/22
# 描述: 工具类API - 词云生成等功能

from flask import Blueprint, request, jsonify
import sys
import os
import logging
import base64
import io
import jieba
from jieba import analyse
from wordcloud import WordCloud

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

tools_bp = Blueprint('tools', __name__)

# 尝试常见的中文字体路径
CHINESE_FONTS = [
    'C:/Windows/Fonts/simhei.ttf',  # Windows 黑体
    'C:/Windows/Fonts/simsun.ttc',  # Windows 宋体
    'C:/Windows/Fonts/simkai.ttf',  # Windows 楷体
    'C:/Windows/Fonts/simfang.ttf', # Windows 仿宋
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # Linux
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    '/System/Library/Fonts/PingFang.ttc',  # macOS
    '/System/Library/Fonts/STHeiti Light.ttc',
]


def get_font_path():
    """获取中文字体文件路径"""
    for font in CHINESE_FONTS:
        if os.path.exists(font):
            logger.info(f"[词云生成] 使用字体: {font}")
            return font
    logger.warning("[词云生成] 未找到中文字体，将使用默认字体")
    return None


@tools_bp.route('/wordcloud', methods=['POST'])
def generate_wordcloud():
    """
    生成词云图片
    参数:
        text: 文本内容 (必填)
        max_words: 最大词数 (可选，默认150)
        width: 图片宽度 (可选，默认1600)
        height: 图片高度 (可选，默认800)
    返回:
        base64编码的词云图片
    """
    try:
        data = request.json
        text = data.get('text', '')
        max_words = data.get('max_words', 150)
        width = data.get('width', 1600)
        height = data.get('height', 800)

        if not text or len(text) < 50:
            return jsonify({
                'code': '400',
                'msg': '文本内容不能为空，且至少需要50个字符',
                'data': None
            }), 400

        logger.info(f"[词云生成] 开始生成，文本长度: {len(text)}, 最大词数: {max_words}")

        # 使用jieba的textrank提取关键词
        keywords = jieba.analyse.textrank(
            text,
            topK=max_words,
            withWeight=False,
            allowPOS=('ns', 'n', 'vn', 'v')
        )

        if not keywords:
            return jsonify({
                'code': '400',
                'msg': '未能从文本中提取到有效关键词',
                'data': None
            }), 400

        # 统计每个关键词出现的次数
        keyword_counts = {}
        for keyword in keywords:
            count = text.count(keyword)
            if count > 0:
                keyword_counts[keyword] = count

        if not keyword_counts:
            return jsonify({
                'code': '400',
                'msg': '关键词统计失败',
                'data': None
            }), 400

        # 获取字体路径
        font_path = get_font_path()
        if not font_path:
            logger.warning("[词云生成] 未找到中文字体，使用默认字体")

        # 创建WordCloud对象
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color='white',
            font_path=font_path,
            max_words=max_words,
            relative_scaling=0.5,
            min_font_size=10,
            max_font_size=150
        )

        # 生成词云
        wordcloud.generate_from_frequencies(keyword_counts)

        # 转换为图片
        img_buffer = io.BytesIO()
        wordcloud.to_image().save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')

        # 准备关键词列表（取前30个）
        sorted_keywords = sorted(
            [{'word': k, 'count': v} for k, v in keyword_counts.items()],
            key=lambda x: x['count'],
            reverse=True
        )[:30]

        logger.info(f"[词云生成] 成功生成，关键词数量: {len(keyword_counts)}")

        response = jsonify({
            'code': '0',
            'msg': '词云生成成功',
            'data': {
                'image_url': f'data:image/png;base64,{img_base64}',
                'keywords': sorted_keywords
            }
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        logger.error(f"[词云生成] 错误: {str(e)}")
        return jsonify({
            'code': '500',
            'msg': f'词云生成失败: {str(e)}',
            'data': None
        }), 500
