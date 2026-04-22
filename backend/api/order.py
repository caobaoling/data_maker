# 文件: api/order.py
# 作者: Claude Code
# 创建日期: 2026/04/22
# 描述: 订单管理API

from flask import Blueprint, request, jsonify
import sys
import os
import logging
import requests
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

order_bp = Blueprint('order', __name__)


@order_bp.route('/add', methods=['POST'])
def add_order():
    """
    添加订单
    参数:
        stu_id: 学员ID (必填)
        order_money: 订单金额 (必填)
        discount_money: 优惠金额 (可选，默认0)
        display_money: 显示金额 (可选)
        goods_id: 商品ID (必填)
        order_type: 订单类型 (可选，默认point_package)
        pay_method: 支付方式 (可选，默认Bank)
        bank: 银行 (可选，默认zh)
        status: 订单状态 (可选，默认on)
        remark: 备注 (可选)
    """
    try:
        data = request.json
        stu_id = data.get('stu_id')
        order_money = data.get('order_money', 1599)
        discount_money = data.get('discount_money', 0)
        display_money = data.get('display_money', order_money)
        goods_id = data.get('goods_id', '263147')
        order_type = data.get('order_type', 'point_package')
        pay_method = data.get('pay_method', 'Bank')
        bank = data.get('bank', 'zh')
        status = data.get('status', 'on')
        remark = data.get('remark', '')

        if not stu_id:
            return jsonify({
                'code': '400',
                'msg': '学员ID不能为空',
                'data': None
            }), 400

        logger.info(f"[添加订单] 开始处理学员ID: {stu_id}")

        # 构建订单数据 - 参考add_order.py的格式
        import time
        import random
        import json
        current_timestamp = int(time.time() * 1000)  # 毫秒级时间戳
        
        order_data = {
            "order_money": order_money,
            "deal_time": datetime.now().strftime('%Y-%m-%d'),
            "cash_card": 649379,
            "remark": remark or "kfdjfd98",
            "content": json.dumps([{"goods_id": int(goods_id), "type": "product"}]),
            "operator": 343,
            "from_url_id": 4793874,
            "bank": bank,
            "user_type": 1,
            "business_type": "51talk",
            "recommend_id": 6878,
            "order_type": order_type,
            "timestamp": current_timestamp,
            "phone_package": 200,
            "from_type": "web",
            "discount_money": discount_money,
            "refund_status": 0,
            "sales_content": json.dumps([{"type": "3", "num": "2", "money": "100"}, {"type": "1", "num": "1", "money": "200"}]),
            "is_new": 0,
            "custom_id": 4422,
            "pay_method": pay_method,
            "discount_type": "cash_down",
            "month_start_date": "2019-03-25",
            "buy_costomer": 7398,
            "app_key": "front",
            "order_num": random.randint(1, 999),
            "gateway": "bank",
            "status": status,
            "remark2": "089ioj",
            "appkey": 60506,
            "display_money": display_money,
            "id": random.randint(100000000, 999999999),
            "stu_id": int(stu_id),
            "extend_id": int(goods_id)
        }

        # 调用订单服务API - 使用params参数而不是json
        url = 'http://172.16.16.97/talkplatform_order_consumer/v1/order/add'
        headers = {
            'Content-Type': 'application/json'
        }

        logger.info(f"[添加订单] 调用API: {url}")
        logger.info(f"[添加订单] 请求数据: {order_data}")

        # 参考原始脚本，使用params参数
        response = requests.post(url, params=order_data, headers=headers, timeout=30)

        logger.info(f"[添加订单] 响应状态码: {response.status_code}")
        logger.info(f"[添加订单] 响应内容: {response.text[:500]}")

        if response.status_code == 200:
            response_data = response.json()
            # API返回code为10000表示成功
            if response_data.get('code') == '10000' or response_data.get('success') == True:
                order_id = response_data.get('id') or response_data.get('order_id')
                logger.info(f"[添加订单] 成功，订单ID: {order_id}")
                return jsonify({
                    'code': '0',
                    'msg': '订单添加成功',
                    'data': {
                        'order_id': order_id,
                        'stu_id': stu_id,
                        'order_money': order_money,
                        'discount_money': discount_money
                    }
                })
            else:
                error_msg = response_data.get('msg', response_data.get('message', '订单添加失败'))
                logger.error(f"[添加订单] API返回错误: {error_msg}")
                return jsonify({
                    'code': '500',
                    'msg': f'订单添加失败: {error_msg}',
                    'data': None
                }), 500
        else:
            logger.error(f"[添加订单] API调用失败，状态码: {response.status_code}")
            return jsonify({
                'code': '500',
                'msg': f'订单服务调用失败，状态码: {response.status_code}',
                'data': None
            }), 500

    except requests.exceptions.Timeout:
        logger.error("[添加订单] API调用超时")
        return jsonify({
            'code': '500',
            'msg': '订单服务调用超时',
            'data': None
        }), 500
    except Exception as e:
        logger.error(f"[添加订单] 未知错误: {str(e)}")
        return jsonify({
            'code': '500',
            'msg': f'操作失败: {str(e)}',
            'data': None
        }), 500
