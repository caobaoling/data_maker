# 文件: app.py
# 作者: Claude Code
# 创建日期: 2026/01/09
# 描述: DataMaker Web平台 Flask后端主应用

from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

# 添加项目根目录到Python路径，以便导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入API蓝图
from api.appoint import appoint_bp
from api.redis import redis_bp
from api.ai_teacher import ai_teacher_bp
from api.elf import elf_bp
from api.picturebook import picturebook_bp
from api.teacher import teacher_bp

# 创建Flask应用
app = Flask(__name__)

# 配置CORS跨域
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # 开发环境允许所有来源，生产环境需限制
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# 注册API蓝图
app.register_blueprint(appoint_bp, url_prefix='/api/appoint')
app.register_blueprint(redis_bp, url_prefix='/api/redis')
app.register_blueprint(ai_teacher_bp, url_prefix='/api/ai')
app.register_blueprint(elf_bp, url_prefix='/api/elf')
app.register_blueprint(picturebook_bp, url_prefix='/api/picturebook')
app.register_blueprint(teacher_bp, url_prefix='/api/teacher')

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'message': 'DataMaker Backend is running',
        'version': '1.0.0'
    })

# 根路径
@app.route('/', methods=['GET'])
def index():
    """根路径欢迎信息"""
    return jsonify({
        'name': 'DataMaker Web Platform API',
        'version': '1.0.0',
        'docs': '/api/health'
    })

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'code': '404',
        'message': 'API endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'code': '500',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # 开发环境运行
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
