# 文件: api/risk.py
# 作者: Claude Code
# 创建日期: 2026/04/22
# 描述: 高风险用户设备管理API

from flask import Blueprint, request, jsonify
import sys
import os
import logging
import requests
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

risk_bp = Blueprint('risk', __name__)

# API基础URL
BASE_URLS = {
    'domestic': 'http://10.0.112.226',  # 境内环境
    'overseas': 'http://192.168.27.35'   # 境外环境
}


def send_request_post(url, params):
    """发送POST请求"""
    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, data=params, headers=headers, timeout=30)
        return response.json()
    except Exception as e:
        logger.error(f"请求失败: {str(e)}")
        return {'code': -1, 'message': f'请求失败: {str(e)}'}


def send_request_get(url, params):
    """发送GET请求"""
    try:
        response = requests.get(url, params=params, timeout=30)
        return response.json()
    except Exception as e:
        logger.error(f"请求失败: {str(e)}")
        return {'code': -1, 'message': f'请求失败: {str(e)}'}


@risk_bp.route('/release', methods=['POST'])
def release_risk():
    """
    解除高风险
    参数:
        env_type: 环境类型 domestic-境内 overseas-境外 (必填)
        stu_id: 学员ID (必填)
        risk_type: 风险类型 1-设备 2-用户 (必填)
        risk_item: 风险项ID (可选，默认使用stu_id)
    """
    try:
        data = request.json
        env_type = data.get('env_type', 'domestic')
        stu_id = data.get('stu_id')
        risk_type = data.get('risk_type', '2')
        risk_item = data.get('risk_item') or stu_id

        if not stu_id:
            return jsonify({
                'code': '400',
                'msg': '学员ID不能为空',
                'data': None
            }), 400

        # 获取对应环境的URL
        base_url = BASE_URLS.get(env_type, BASE_URLS['domestic'])
        env_name = '境内' if env_type == 'domestic' else '境外'

        logger.info(f"[解除高风险] 环境: {env_name}({base_url}), 学员ID: {stu_id}, 风险类型: {risk_type}, 风险项: {risk_item}")

        # 构建请求参数
        timestamp_seconds = int(time.time())
        release_params = {
            'stu_id': int(stu_id),
            'risk_type': risk_type,
            'appkey': 'erp',
            'timestamp': timestamp_seconds,
            'risk_item': risk_item,
            'status': '2'
        }

        # 调用解除高风险API
        release_url = f'{base_url}/api/high_risk_user_device/release'
        logger.info(f"[解除高风险] 调用API: {release_url}")
        logger.info(f"[解除高风险] 请求参数: {release_params}")

        response_data = send_request_post(release_url, release_params)
        logger.info(f"[解除高风险] 响应数据: {response_data}")

        if response_data.get('code') == 10000:
            logger.info(f"[解除高风险] 成功")
            return jsonify({
                'code': '0',
                'msg': '解除高风险成功',
                'data': response_data
            })
        else:
            error_msg = response_data.get('message', '解除高风险失败')
            logger.error(f"[解除高风险] 失败: {error_msg}")
            return jsonify({
                'code': '500',
                'msg': f'解除高风险失败: {error_msg}',
                'data': response_data
            }), 500

    except Exception as e:
        logger.error(f"[解除高风险] 未知错误: {str(e)}")
        return jsonify({
            'code': '500',
            'msg': f'操作失败: {str(e)}',
            'data': None
        }), 500


@risk_bp.route('/whitelist', methods=['POST'])
def add_whitelist():
    """
    添加白名单
    参数:
        env_type: 环境类型 domestic-境内 overseas-境外 (必填)
        stu_id: 学员ID (必填)
        risk_type: 风险类型 1-设备 2-用户 (必填)
        risk_item: 风险项ID (可选，默认使用stu_id)
    """
    try:
        data = request.json
        env_type = data.get('env_type', 'domestic')
        stu_id = data.get('stu_id')
        risk_type = data.get('risk_type', '2')
        risk_item = data.get('risk_item') or stu_id

        if not stu_id:
            return jsonify({
                'code': '400',
                'msg': '学员ID不能为空',
                'data': None
            }), 400

        # 获取对应环境的URL
        base_url = BASE_URLS.get(env_type, BASE_URLS['domestic'])
        env_name = '境内' if env_type == 'domestic' else '境外'

        logger.info(f"[添加白名单] 环境: {env_name}({base_url}), 学员ID: {stu_id}, 风险类型: {risk_type}, 风险项: {risk_item}")

        # 构建请求参数
        timestamp_seconds = int(time.time())
        operator_id = '124'
        whitelist_params = {
            'appkey': 'erp',
            'timestamp': timestamp_seconds,
            'risk_type': risk_type,
            'risk_item': risk_item,
            'operator_id': operator_id
        }

        # 调用添加白名单API
        whitelist_url = f'{base_url}/api/high_risk_user_device/add_white_list'
        logger.info(f"[添加白名单] 调用API: {whitelist_url}")
        logger.info(f"[添加白名单] 请求参数: {whitelist_params}")

        response_data = send_request_get(whitelist_url, whitelist_params)
        logger.info(f"[添加白名单] 响应数据: {response_data}")

        if response_data.get('code') == 10000:
            logger.info(f"[添加白名单] 成功")
            return jsonify({
                'code': '0',
                'msg': '添加白名单成功',
                'data': response_data
            })
        else:
            error_msg = response_data.get('message', '添加白名单失败')
            logger.error(f"[添加白名单] 失败: {error_msg}")
            return jsonify({
                'code': '500',
                'msg': f'添加白名单失败: {error_msg}',
                'data': response_data
            }), 500

    except Exception as e:
        logger.error(f"[添加白名单] 未知错误: {str(e)}")
        return jsonify({
            'code': '500',
            'msg': f'操作失败: {str(e)}',
            'data': None
        }), 500
