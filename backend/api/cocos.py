# 文件: api/cocos.py
# 作者: bao0
# 创建日期: 2026/07/13
# 描述: cocos 课后出题校验 API

from flask import Blueprint, request, Response, jsonify
import sys
import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cocos_bp = Blueprint('cocos', __name__)

# 项目根目录（backend 的上一级）
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
SCRIPT_PATH  = os.path.join(PROJECT_ROOT, 'cocos', 'verify_mastery.py')


@cocos_bp.route('/verify_mastery', methods=['POST'])
def verify_mastery():
    """
    执行 cocos/verify_mastery.py，流式返回脚本输出。

    请求体 (JSON):
        appoint_id   : str  必填，约课ID
        lesson_type  : str  选填，课程类型（课型-en，如 reading_class）
        lesson_level : str  选填，课程级别（如 Level 2）

    响应: text/plain 流式输出（每行即时推送）
    """
    data = request.get_json(silent=True) or {}
    appoint_id   = str(data.get('appoint_id', '')).strip()
    lesson_type  = str(data.get('lesson_type', '')).strip()
    lesson_level = str(data.get('lesson_level', '')).strip()

    if not appoint_id:
        return jsonify({'code': '400', 'msg': 'appoint_id 不能为空', 'data': None}), 400

    # 构造命令行参数
    cmd = [sys.executable, SCRIPT_PATH, appoint_id]
    if lesson_type and lesson_level:
        cmd += [lesson_type, lesson_level]

    logger.info(f"[cocos] 执行命令: {' '.join(cmd)}")

    def generate():
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=PROJECT_ROOT,
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'},
                bufsize=1,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace',
            )
            for line in proc.stdout:
                yield line
            proc.wait()
            if proc.returncode != 0:
                yield f'\n[错误] 脚本退出码: {proc.returncode}\n'
        except Exception as e:
            logger.error(f"[cocos] 执行异常: {e}")
            yield f'[异常] {str(e)}\n'

    return Response(generate(), mimetype='text/plain; charset=utf-8')
