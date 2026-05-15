# 文件: api/user.py
# 作者: Claude Code
# 创建日期: 2026/03/12
# 描述: 用户管理工具API

from flask import Blueprint, request, jsonify
import sys
import os
import logging
import re
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.db_connect import create_connection
from common.get_crm_session import CRMClient

user_bp = Blueprint('user', __name__)

# CRM账号配置
CRM_ACCOUNTS = {
    'test': {'username': 'admin', 'password': '51talk20250227#'},
    'prod': {'username': 'caobaoling', 'password': 'Test123$'}
}

def get_crm_client(env='test', base_url='https://crm.51suyang.cn'):
    """根据环境获取对应账号的CRMClient"""
    account = CRM_ACCOUNTS.get(env, CRM_ACCOUNTS['test'])
    return CRMClient(username=account['username'], password=account['password'], base_url=base_url)

# 财富类型配置
WEALTH_TYPES = {
    'point': {'sku_id': 1, 'name': '次卡'},
    'classtime': {'sku_id': 19, 'name': '课时'},
    'pthpoint': {'sku_id': 104, 'name': '普通话'},
    'ar_point': {'sku_id': 109, 'name': '阿教次卡'},
    'ai_podcast': {'sku_id': 117, 'name': 'AI播客'},
    'academy': {'sku_id': 116, 'name': '中东学院'},
    'ai_teach': {'sku_id': 113, 'name': 'AI外教'},
    'pbook': {'sku_id': 106, 'name': '51绘本'},
    'word1v1': {'sku_id': 111, 'name': '正课课时'},
    'word_review1v1': {'sku_id': 112, 'name': '抗遗忘课时'},
    'jp_point': {'sku_id': 108, 'name': '日本本地课时'}
}

@user_bp.route('/add_wealth', methods=['POST'])
def add_wealth():
    """
    为用户添加财富
    参数:
        user_id: 用户ID (必填)
        sku_type: 财富类型 (必填)
        count: 数量 (可选，默认100)
        days: 有效天数 (可选，默认300)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        sku_type = data.get('sku_type')
        count = data.get('count', 100.00)
        days = data.get('days', 300)

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        if not sku_type:
            return jsonify({
                'code': '400',
                'msg': '财富类型不能为空',
                'data': None
            }), 400

        if sku_type not in WEALTH_TYPES:
            return jsonify({
                'code': '400',
                'msg': f'不支持的财富类型: {sku_type}',
                'data': None
            }), 400

        wealth_config = WEALTH_TYPES[sku_type]
        sku_id = wealth_config['sku_id']
        wealth_name = wealth_config['name']

        # 计算有效期
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

        logger.info(f"[添加财富] 用户ID: {user_id}, 类型: {wealth_name}({sku_type}), 数量: {count}, 有效期: {days}天")

        conn = create_connection()
        cursor = conn.cursor()

        try:
            # 插入财富记录
            add_query = """
                INSERT INTO `point`.`user_assets`
                (`stu_id`, `count`, `sku_id`, `sku_type`, `valid_start`, `valid_end`, `days`)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(add_query, (user_id, count, sku_id, sku_type, start_date, end_date, days))
            conn.commit()

            logger.info(f"[添加财富] 成功添加 {count} {wealth_name} 到用户 {user_id}")

            return jsonify({
                'code': '0',
                'msg': f'成功添加 {count} {wealth_name}',
                'data': {
                    'user_id': user_id,
                    'sku_type': sku_type,
                    'sku_id': sku_id,
                    'wealth_name': wealth_name,
                    'count': count,
                    'valid_start': start_date,
                    'valid_end': end_date,
                    'days': days
                }
            })

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"[添加财富] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'添加失败: {str(e)}',
            'data': None
        }), 500

@user_bp.route('/query_wealth', methods=['POST'])
def query_wealth():
    """
    查询用户财富
    参数:
        user_id: 用户ID (必填)
        sku_type: 财富类型 (可选，不传则查询所有类型)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        sku_type = data.get('sku_type')

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        logger.info(f"[查询财富] 用户ID: {user_id}, 类型: {sku_type or '全部'}")

        conn = create_connection()
        cursor = conn.cursor()

        try:
            # 构建查询SQL
            if sku_type:
                if sku_type not in WEALTH_TYPES:
                    return jsonify({
                        'code': '400',
                        'msg': f'不支持的财富类型: {sku_type}',
                        'data': None
                    }), 400

                query = """
                    SELECT id, stu_id, count, sku_id, sku_type, valid_start, valid_end, days, status
                    FROM `point`.`user_assets`
                    WHERE stu_id = %s AND sku_type = %s
                    ORDER BY id DESC
                """
                cursor.execute(query, (user_id, sku_type))
            else:
                query = """
                    SELECT id, stu_id, count, sku_id, sku_type, valid_start, valid_end, days, status
                    FROM `point`.`user_assets`
                    WHERE stu_id = %s
                    ORDER BY sku_type, id DESC
                """
                cursor.execute(query, (user_id,))

            results = cursor.fetchall()

            assets = []
            total_count = 0
            for row in results:
                asset = {
                    'id': row[0],
                    'user_id': row[1],
                    'count': float(row[2]),
                    'sku_id': row[3],
                    'sku_type': row[4],
                    'wealth_name': WEALTH_TYPES.get(row[4], {}).get('name', '未知类型'),
                    'valid_start': str(row[5]),
                    'valid_end': str(row[6]),
                    'days': row[7],
                    'status': row[8]
                }
                assets.append(asset)
                total_count += float(row[2])

            logger.info(f"[查询财富] 用户 {user_id} 共有 {len(assets)} 条记录，总计 {total_count}")

            return jsonify({
                'code': '0',
                'msg': '查询成功',
                'data': {
                    'user_id': user_id,
                    'total_count': total_count,
                    'assets': assets
                }
            })

        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"[查询财富] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'查询失败: {str(e)}',
            'data': None
        }), 500

@user_bp.route('/wealth_types', methods=['GET'])
def get_wealth_types():
    """
    获取所有支持的财富类型
    """
    try:
        types_list = [
            {
                'sku_type': key,
                'sku_id': value['sku_id'],
                'name': value['name']
            }
            for key, value in WEALTH_TYPES.items()
        ]

        return jsonify({
            'code': '0',
            'msg': '获取成功',
            'data': types_list
        })
    except Exception as e:
        logger.error(f"[获取财富类型] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'获取失败: {str(e)}',
            'data': None
        }), 500


def parse_php_vardump(text):
    """
    解析 PHP var_dump 格式文本，提取键值对
    示例输入: 'array(3) {\n  ["code"]=>\n  string(5) "10000"\n  ...\n}\nNULL\n'
    返回: {'code': '10000', 'message': '用户属性', 'res': '1'}
    """
    import re
    result = {}
    pattern = re.compile(r'\["(\w+)"\]=>\s*\w+\(\d+\)\s*"([^"]*)"')
    for match in pattern.finditer(text):
        result[match.group(1)] = match.group(2)
    return result if result else {'raw': text.strip()}


# 阿语标签类型配置
ARABIC_TAG_TYPES = {
    'ar_tea': {'name': '阿语意向', 'desc': '标记学员有阿语学习意向'},
    'ar_point': {'name': '已付费阿语订单', 'desc': '标记学员已购买阿语课程'}
}

@user_bp.route('/arabic_tag_types', methods=['GET'])
def get_arabic_tag_types():
    """
    获取阿语标签类型列表
    """
    try:
        types_list = [
            {
                'type': key,
                'name': value['name'],
                'desc': value['desc']
            }
            for key, value in ARABIC_TAG_TYPES.items()
        ]

        return jsonify({
            'code': '0',
            'msg': '获取成功',
            'data': types_list
        })
    except Exception as e:
        logger.error(f"[获取阿语标签类型] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'获取失败: {str(e)}',
            'data': None
        }), 500


@user_bp.route('/arabic_tag/query', methods=['POST'])
def query_arabic_tag():
    """
    查询用户阿语标签
    参数:
        user_id: 用户ID (必填)
        type: 标签类型 (必填，ar_tea/ar_point)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        tag_type = data.get('type')

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        if not tag_type:
            return jsonify({
                'code': '400',
                'msg': '标签类型不能为空',
                'data': None
            }), 400

        if tag_type not in ARABIC_TAG_TYPES:
            return jsonify({
                'code': '400',
                'msg': f'不支持的标签类型: {tag_type}',
                'data': None
            }), 400

        logger.info(f"[查询阿语标签] 用户ID: {user_id}, 类型: {tag_type}")

        # 使用 CRMClient session 调用接口（需要登录态）
        client = CRMClient()
        session = client.get_session()
        if not session:
            return jsonify({
                'code': '500',
                'msg': '登录失败，无法获取session',
                'data': None
            }), 500

        url = 'https://www.51talk.com/Admin/Masy/getAttributeBySid'
        params = {'user_id': user_id, 'type': tag_type}
        response = session.get(url, params=params, verify=False, timeout=15)
        response.encoding = 'utf-8'
        result = parse_php_vardump(response.text)
        client.close()

        logger.info(f"[查询阿语标签] 结果: {result}")

        return jsonify({
            'code': '0',
            'msg': '查询成功',
            'data': {
                'user_id': user_id,
                'type': tag_type,
                'type_name': ARABIC_TAG_TYPES[tag_type]['name'],
                'result': result
            }
        })

    except Exception as e:
        logger.error(f"[查询阿语标签] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'查询失败: {str(e)}',
            'data': None
        }), 500


@user_bp.route('/get_mobile', methods=['POST'])
def get_mobile():
    """
    通过用户ID获取手机号
    参数:
        user_id: 用户ID (必填)
        region: 用户区域 (可选，domestic=境内/overseas=境外，默认domestic)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        env = data.get('env', 'test')

        if not user_id:
            return jsonify({'code': '400', 'msg': '用户ID不能为空', 'data': None}), 400

        logger.info(f"[获取手机号] 用户ID: {user_id}, 环境: {env}")

        base_domain = 'crm.51suyang.cn'
        client = get_crm_client(env, base_url=f'https://{base_domain}')
        session = client.get_session()
        if not session:
            return jsonify({'code': '500', 'msg': '登录失败，无法获取session', 'data': None}), 500

        # 第一步：访问 update_email.php 页面，从 HTML 提取真实的 stu_id
        page_url = f'https://{base_domain}/admin/user/update_email.php'
        page_resp = session.get(page_url, params={'user_id': user_id}, verify=False, timeout=15)
        page_resp.encoding = 'utf-8'

        match = re.search(r"showUserView\('(\d+)',\s*'mobile'\)", page_resp.text)
        if not match:
            client.close()
            return jsonify({'code': '500', 'msg': '无法从页面提取stu_id，请确认用户ID是否正确', 'data': None}), 500

        stu_id = match.group(1)
        logger.info(f"[获取手机号] 提取到 stu_id: {stu_id}")

        # 第二步：用 stu_id 调用接口获取手机号
        api_url = f'https://{base_domain}/admin/user/ajax_get_current_field.php'
        response = session.post(api_url, data={'stu_id': stu_id, 'field': 'mobile'}, verify=False, timeout=15)
        response.encoding = 'utf-8'
        client.close()

        mobile = response.text.strip()
        logger.info(f"[获取手机号] 响应: {mobile}")

        return jsonify({
            'code': '0',
            'msg': '获取成功',
            'data': {
                'user_id': user_id,
                'mobile': mobile
            }
        })

    except Exception as e:
        logger.error(f"[获取手机号] 错误: {e}")
        return jsonify({'code': '500', 'msg': f'获取失败: {str(e)}', 'data': None}), 500


@user_bp.route('/add_overseas_label', methods=['POST'])
def add_overseas_label():
    """
    为用户打海外标签
    参数:
        user_id: 用户ID (必填)
        country_code: 国家代码 (可选，默认886)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        country_code = data.get('country_code', '886')
        env = data.get('env', 'test')

        if not user_id:
            return jsonify({'code': '400', 'msg': '用户ID不能为空', 'data': None}), 400

        logger.info(f"[打海外标签] 用户ID: {user_id}, country_code: {country_code}, 环境: {env}")

        client = get_crm_client(env, base_url='https://crm.51talk.com')
        session = client.get_session()
        if not session:
            return jsonify({'code': '500', 'msg': '登录失败，无法获取session', 'data': None}), 500

        url = f'https://junior.51talk.com/admin/Tools/addGlobalLabel'
        params = {'id': user_id, 'country_code': country_code}
        response = session.get(url, params=params, verify=False, timeout=15)
        response.encoding = 'utf-8'
        client.close()

        logger.info(f"[打海外标签] 响应: {response.text[:200]}")

        return jsonify({
            'code': '0',
            'msg': '操作成功',
            'data': {
                'user_id': user_id,
                'country_code': country_code,
                'raw': response.text
            }
        })

    except Exception as e:
        logger.error(f"[打海外标签] 错误: {e}")
        return jsonify({'code': '500', 'msg': f'操作失败: {str(e)}', 'data': None}), 500


@user_bp.route('/unlock_account', methods=['POST'])
def unlock_account():
    """
    通过手机号解锁账户
    参数:
        username: 手机号或用户ID (必填)
        region: 用户区域 (可选，domestic=境内/overseas=境外，默认domestic)
    """
    try:
        data = request.json
        username = data.get('username')
        region = data.get('region', 'domestic')
        env = data.get('env', 'test')

        if not username:
            return jsonify({'code': '400', 'msg': '用户ID不能为空', 'data': None}), 400

        logger.info(f"[解锁账户] username: {username}, 区域: {region}, 环境: {env}")

        base_domain = 'crm.51suyang.cn' if region == 'domestic' else 'crm.51talk.com'
        client = get_crm_client(env, base_url=f'https://{base_domain}')
        session = client.get_session()
        if not session:
            return jsonify({'code': '500', 'msg': '登录失败，无法获取session', 'data': None}), 500

        url = f'https://{base_domain}/Admin/Sso/password'
        params = {'username': username}
        response = session.get(url, params=params, verify=False, timeout=15)
        response.encoding = 'utf-8'
        client.close()

        logger.info(f"[解锁账户] 响应: {response.text[:200]}")

        return jsonify({
            'code': '0',
            'msg': '解锁操作已发送',
            'data': {
                'username': username,
                'region': region,
                'raw': response.text
            }
        })

    except Exception as e:
        logger.error(f"[解锁账户] 错误: {e}")
        return jsonify({'code': '500', 'msg': f'解锁失败: {str(e)}', 'data': None}), 500


@user_bp.route('/arabic_tag/add', methods=['POST'])
def add_arabic_tag():
    """
    为用户添加阿语标签
    参数:
        user_id: 用户ID (必填)
        type: 标签类型 (必填，ar_tea/ar_point)
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        tag_type = data.get('type')

        if not user_id:
            return jsonify({
                'code': '400',
                'msg': '用户ID不能为空',
                'data': None
            }), 400

        if not tag_type:
            return jsonify({
                'code': '400',
                'msg': '标签类型不能为空',
                'data': None
            }), 400

        if tag_type not in ARABIC_TAG_TYPES:
            return jsonify({
                'code': '400',
                'msg': f'不支持的标签类型: {tag_type}',
                'data': None
            }), 400

        logger.info(f"[添加阿语标签] 用户ID: {user_id}, 类型: {tag_type}")

        # 使用 CRMClient session 调用接口（需要登录态）
        client = CRMClient()
        session = client.get_session()
        if not session:
            return jsonify({
                'code': '500',
                'msg': '登录失败，无法获取session',
                'data': None
            }), 500

        url = 'https://www.51talk.com/Admin/Masy/getAttributeBySid'
        params = {'user_id': user_id, 'type': tag_type, 'action': 1}
        response = session.get(url, params=params, verify=False, timeout=15)
        response.encoding = 'utf-8'
        result = parse_php_vardump(response.text)
        client.close()

        logger.info(f"[添加阿语标签] 结果: {result}")

        return jsonify({
            'code': '0',
            'msg': '添加成功',
            'data': {
                'user_id': user_id,
                'type': tag_type,
                'type_name': ARABIC_TAG_TYPES[tag_type]['name'],
                'result': result
            }
        })

    except Exception as e:
        logger.error(f"[添加阿语标签] 错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'添加失败: {str(e)}',
            'data': None
        }), 500

