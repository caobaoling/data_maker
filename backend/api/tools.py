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
import platform  # 新增：用于检测系统类型

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

tools_bp = Blueprint('tools', __name__)

# ========== 优化后的中文字体路径配置 ==========
# 1. 按优先级排序：系统默认字体 > 通用字体目录 > 项目自定义字体目录
# 2. 覆盖 Windows（多语言版本）、Linux（主流发行版）、macOS
CHINESE_FONTS = [
    # Windows 系统（含英文/中文版本）
    'C:/Windows/Fonts/simhei.ttf',      # 黑体
    'C:/Windows/Fonts/simsun.ttc',      # 宋体
    'C:/Windows/Fonts/msyh.ttc',        # 微软雅黑
    'C:/Windows/Fonts/STSong.ttf',      # 华文宋体
    'C:\\WINNT\\Fonts\\simhei.ttf',     # Windows 2000/XP 兼容
    # Linux 系统（主流发行版：Ubuntu/CentOS/Debian）
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',    # 文泉驿正黑
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # 文泉驿微米黑
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',  # 通用无衬线字体
    '/usr/share/fonts/zh_CN/TrueType/simhei.ttf',      # CentOS 中文字体
    '/usr/share/fonts/ChineseFonts/simhei.ttf',        # 自定义安装的中文字体
    '/usr/local/share/fonts/simhei.ttf',               # 本地安装字体
    # macOS 系统
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/Library/Fonts/Microsoft YaHei.ttc',
    # 项目自定义字体目录（建议将字体文件放到项目中，兜底使用）
    os.path.join(os.path.dirname(__file__), '../../fonts/simhei.ttf'),
    os.path.join(os.path.dirname(__file__), '../fonts/simhei.ttf'),
    './fonts/simhei.ttf'
]

# 新增：Linux 通用字体搜索目录（兜底扫描）
LINUX_FONT_DIRS = [
    '/usr/share/fonts',
    '/usr/local/share/fonts',
    '~/.fonts',
    '/usr/share/fonts/zh_CN',
    '/usr/share/fonts/truetype'
]


def search_linux_chinese_font():
    """Linux 系统下递归搜索中文字体文件"""
    target_fonts = ['simhei.ttf', 'wqy-zenhei.ttc', 'wqy-microhei.ttc', 'msyh.ttc']
    for font_dir in LINUX_FONT_DIRS:
        font_dir = os.path.expanduser(font_dir)  # 解析 ~ 目录
        if not os.path.exists(font_dir):
            continue
        # 递归遍历目录
        for root, dirs, files in os.walk(font_dir):
            for file in files:
                if file.lower() in [f.lower() for f in target_fonts]:
                    font_path = os.path.join(root, file)
                    logger.info(f"[词云生成] Linux 搜索到字体: {font_path}")
                    return font_path
    return None


def get_font_path():
    """获取中文字体文件路径（适配 Windows/Linux/macOS）"""
    # 第一步：优先检测预配置的字体路径
    for font in CHINESE_FONTS:
        font_path = os.path.abspath(font)
        if os.path.exists(font_path):
            logger.info(f"[词云生成] 使用预配置字体: {font_path}")
            return font_path

    # 第二步：根据系统类型针对性搜索
    system = platform.system().lower()
    if system == 'linux':
        # Linux 系统递归搜索字体
        linux_font = search_linux_chinese_font()
        if linux_font:
            return linux_font
    elif system == 'windows':
        # Windows 系统补充搜索 Fonts 目录（兼容不同语言版本）
        win_font_dirs = [
            os.environ.get('WINDIR', 'C:/Windows') + '/Fonts',
            'C:/WINNT/Fonts'
        ]
        win_target_fonts = ['simhei.ttf', 'simsun.ttc', 'msyh.ttc']
        for font_dir in win_font_dirs:
            for font_file in win_target_fonts:
                font_path = os.path.join(font_dir, font_file)
                if os.path.exists(font_path):
                    logger.info(f"[词云生成] Windows 搜索到字体: {font_path}")
                    return font_path

    # 第三步：未找到字体的警告
    logger.warning("[词云生成] 未找到中文字体文件，将使用WordCloud默认字体（可能显示乱码）")
    return None

# ========== 以下原有代码无需修改 ==========
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