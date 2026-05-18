# 文件: api/teacher.py
# 作者: Claude Code
# 创建日期: 2026/03/06
# 描述: 外教管理工具API

from flask import Blueprint, request, jsonify
import sys
import os
import logging
import re
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.db_connect import create_connection
from common.get_crm_session import CRMClient
from common.env_utils import get_request_with_host_override

teacher_bp = Blueprint('teacher', __name__)


def insert_contract_to_db(teacher_id):
    """
    步骤1: 插入合同记录到数据库
    返回: (是否成功, 日志消息)
    """
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # 先检查该老师是否已经存在type=3的合同记录
        check_query = """
            SELECT COUNT(*) FROM `talk`.`teacher_contract`
            WHERE t_id = %s AND type = 3
        """
        cursor.execute(check_query, (teacher_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            log_msg = f"老师 {teacher_id} 已存在type=3的合同记录，跳过数据库插入"
            logger.info(f"[步骤1-数据库插入] {log_msg}")
            return (True, log_msg)
        else:
            # 插入teacher_contract记录
            insert_query = """
                INSERT INTO `talk`.`teacher_contract`
                (`t_id`, `first_name`, `middle_name`, `last_name`, `birthday`, `email`,
                 `post_address`, `city`, `province`, `regional_des`, `region`, `island`,
                 `zip_code`, `img`, `add_time`, `type`, `sa_version`, `contract_party`)
                VALUES (%s, 'Joey', 'Mendoza', 'Ubias', '12/28/1990', 'joeymarkubias@hotmail.ph',
                        '32B Caggay, Soldiers Hill, Tuguegarao City, Cagayan', 0, 0, 0, 0, 0,
                        '3500', NULL, %s, 3, 0, 0)
            """
            add_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(insert_query, (teacher_id, add_time))
            conn.commit()

            log_msg = f"成功插入数据库，老师ID: {teacher_id}"
            logger.info(f"[步骤1-数据库插入] {log_msg}")
            return (True, log_msg)

    except Exception as e:
        conn.rollback()
        log_msg = f"数据库操作失败: {str(e)}"
        logger.error(f"[步骤1-数据库插入] {log_msg}")
        return (False, log_msg)
    finally:
        cursor.close()
        conn.close()


def update_crm_sa_end_time(teacher_id):
    """
    步骤2: 调用CRM接口更新sa_end_time (自动适配测试/生产环境)
    返回: (是否成功, 日志消息, sa_end_time值)
    """
    client = None
    try:
        # 计算当前时间+2年
        sa_end_time = (datetime.now() + relativedelta(years=2)).strftime('%Y-%m-%d 23:59:59')

        # 使用 CRMClient 获取 Session
        client = CRMClient()
        session = client.get_session()
        if not session:
            log_msg = "CRM登录失败,无法获取有效Session"
            logger.error(f"[步骤2-CRM接口] {log_msg}")
            return (False, log_msg, sa_end_time)

        crm_url = 'https://tms.51talk.com/tea_promotion/batchUpdateTeacherInfo'
        params = {
            't_ids': teacher_id,
            'field': 'sa_end_time',
            'value': sa_end_time,
            'do': '1'
        }

        logger.info(f"[步骤2-CRM接口] 调用接口更新sa_end_time")

        # 使用环境适配方法发送请求
        response = get_request_with_host_override(
            session,
            crm_url,
            method='GET',
            params=params,
            timeout=30,
            verify=False
        )

        logger.info(f"[步骤2-CRM接口] 响应状态码: {response.status_code}, 响应内容: {response.text[:500]}")

        if response.status_code == 200:
            response_text = response.text.strip()

            # 优先检查权限错误
            if 'no permission' in response_text.lower():
                log_msg = f"CRM接口权限不足: {response_text}"
                logger.error(f"[步骤2-CRM接口] {log_msg}")
                return (False, log_msg, sa_end_time)

            # 检查是否包含xdebug调试信息(说明接口调用成功,只是返回了调试信息)
            if 'xdebug-var-dump' in response_text and str(teacher_id) in response_text:
                log_msg = f"成功更新CRM，老师ID: {teacher_id}, sa_end_time: {sa_end_time} (接口返回调试信息)"
                logger.info(f"[步骤2-CRM接口] {log_msg}")
                return (True, log_msg, sa_end_time)

            # 尝试解析JSON响应
            try:
                response_data = response.json()
                # 检查CRM接口返回的业务状态
                if response_data.get('status') == 1 or response_data.get('code') == 0:
                    log_msg = f"成功更新CRM，老师ID: {teacher_id}, sa_end_time: {sa_end_time}"
                    logger.info(f"[步骤2-CRM接口] {log_msg}")
                    return (True, log_msg, sa_end_time)
                else:
                    log_msg = f"CRM接口返回业务错误: {response_data.get('msg', '未知错误')}"
                    logger.error(f"[步骤2-CRM接口] {log_msg}, 完整响应: {response.text}")
                    return (False, log_msg, sa_end_time)
            except Exception as json_error:
                # 如果不是JSON格式,检查是否包含成功标识
                if 'success' in response_text.lower() or 'ok' in response_text.lower():
                    log_msg = f"成功更新CRM，老师ID: {teacher_id}, sa_end_time: {sa_end_time}"
                    logger.info(f"[步骤2-CRM接口] {log_msg}")
                    return (True, log_msg, sa_end_time)
                else:
                    log_msg = f"CRM接口返回非预期响应: {response_text[:200]}"
                    logger.error(f"[步骤2-CRM接口] {log_msg}")
                    return (False, log_msg, sa_end_time)
        else:
            log_msg = f"CRM接口返回错误状态码: {response.status_code}, 响应: {response.text[:200]}"
            logger.error(f"[步骤2-CRM接口] {log_msg}")
            return (False, log_msg, sa_end_time)

    except requests.exceptions.Timeout:
        log_msg = "CRM接口调用超时"
        logger.error(f"[步骤2-CRM接口] {log_msg}")
        return (False, log_msg, None)
    except Exception as e:
        log_msg = f"CRM接口调用失败: {str(e)}"
        logger.error(f"[步骤2-CRM接口] {log_msg}")
        return (False, log_msg, None)


@teacher_bp.route('/add_contract', methods=['POST'])
def add_contract():
    """
    为老师添加合同(SA)
    参数:
        teacher_id: 老师ID (必填)
    操作:
        1. 插入数据库记录到 talk.teacher_contract
        2. 调用CRM接口更新sa_end_time
    """
    try:
        data = request.json
        teacher_id = data.get('teacher_id')

        if not teacher_id:
            return jsonify({
                'code': '400',
                'msg': '老师ID不能为空',
                'data': None
            }), 400

        logger.info(f"[添加合同] 开始处理老师ID: {teacher_id}")

        result = {
            'teacher_id': teacher_id,
            'steps': [],
            'success': False
        }

        # 步骤1: 插入数据库记录
        db_success, db_log = insert_contract_to_db(teacher_id)
        result['steps'].append({
            'step': 1,
            'name': '数据库插入',
            'success': db_success,
            'log': db_log
        })

        # 步骤2: 调用CRM接口
        crm_success, crm_log, sa_end_time = update_crm_sa_end_time(teacher_id)
        result['steps'].append({
            'step': 2,
            'name': 'CRM接口调用',
            'success': crm_success,
            'log': crm_log,
            'sa_end_time': sa_end_time
        })

        # 判断整体成功: CRM成功即为成功(即使DB跳过插入)
        result['success'] = crm_success
        result['db_insert'] = db_success
        result['crm_update'] = crm_success

        if result['success']:
            result['message'] = f"操作完成，老师ID: {teacher_id}"
            return jsonify({
                'code': '0',
                'msg': '操作成功',
                'data': result
            })
        else:
            result['message'] = "TMS接口调用失败"
            return jsonify({
                'code': '500',
                'msg': result['message'],
                'data': result
            }), 500

    except Exception as e:
        logger.error(f"[添加合同] 未知错误: {e}")
        return jsonify({
            'code': '500',
            'msg': f'操作失败: {str(e)}',
            'data': None
        }), 500


@teacher_bp.route('/get_email', methods=['POST'])
def get_teacher_email():
    """
    获取老师邮箱
    参数:
        teacher_id: 老师ID (必填)
    操作:
        调用TMS接口 https://tms.51talk.com/tea/show_reveal_info 查询老师邮箱
    """
    try:
        data = request.json
        teacher_id = data.get('teacher_id')

        if not teacher_id:
            return jsonify({
                'code': '400',
                'msg': '老师ID不能为空',
                'data': None
            }), 400

        logger.info(f"[获取老师邮箱] 开始查询老师ID: {teacher_id}")

        # 使用 CRMClient 获取 Session
        client = CRMClient()
        session = client.get_session()
        if not session:
            logger.error("[获取老师邮箱] CRM登录失败,无法获取有效Session")
            return jsonify({
                'code': '500',
                'msg': 'CRM登录失败，无法获取有效Session',
                'data': None
            }), 500

        tms_url = 'https://tms.51talk.com/tea/show_reveal_info'
        params = {
            'type': 'email',
            'teacherID': teacher_id
        }

        logger.info(f"[获取老师邮箱] 调用TMS接口: {tms_url}, 参数: {params}")

        # 使用环境适配方法发送请求 - POST请求使用data参数
        response = get_request_with_host_override(
            session,
            tms_url,
            method='POST',
            data=params,
            timeout=30,
            verify=False
        )
        logger.info(f"[获取老师邮箱] 响应状态码: {response.status_code}")
        logger.info(f"[获取老师邮箱] 响应内容: {response.text[:500]}")

        if response.status_code == 200:
            try:
                response_data = response.json()
                logger.info(f"[获取老师邮箱] 响应数据: {response_data}")
                
                # 检查接口返回状态 - status 为 1 表示成功
                if response_data.get('status') == 1 or response_data.get('status') == 'success':
                    # TMS接口返回的邮箱在info字段
                    email = response_data.get('info') or response_data.get('data', {}).get('email') or response_data.get('email')
                    if email:
                        logger.info(f"[获取老师邮箱] 成功获取邮箱: {email}")
                        return jsonify({
                            'code': '0',
                            'msg': '查询成功',
                            'data': {
                                'teacher_id': teacher_id,
                                'email': email
                            }
                        })
                    else:
                        logger.warning(f"[获取老师邮箱] 接口返回成功但未找到邮箱数据")
                        return jsonify({
                            'code': '404',
                            'msg': '未找到该老师的邮箱信息',
                            'data': None
                        })
                else:
                    error_msg = response_data.get('info') or response_data.get('msg') or response_data.get('message', '查询失败')
                    logger.error(f"[获取老师邮箱] 接口返回错误: {error_msg}")
                    return jsonify({
                        'code': '500',
                        'msg': f'查询失败: {error_msg}',
                        'data': None
                    }), 500
            except Exception as e:
                logger.error(f"[获取老师邮箱] 解析响应失败: {str(e)}")
                return jsonify({
                    'code': '500',
                    'msg': f'解析响应失败: {str(e)}',
                    'data': None
                }), 500
        else:
            logger.error(f"[获取老师邮箱] 接口返回错误状态码: {response.status_code}")
            return jsonify({
                'code': '500',
                'msg': f'接口调用失败，状态码: {response.status_code}',
                'data': None
            }), 500

    except requests.exceptions.Timeout:
        logger.error("[获取老师邮箱] TMS接口调用超时")
        return jsonify({
            'code': '500',
            'msg': 'TMS接口调用超时',
            'data': None
        }), 500
    except Exception as e:
        logger.error(f"[获取老师邮箱] 未知错误: {str(e)}")
        return jsonify({
            'code': '500',
            'msg': f'操作失败: {str(e)}',
            'data': None
        }), 500


@teacher_bp.route('/reset_password', methods=['POST'])
def reset_teacher_password():
    """
    重置老师密码
    参数:
        teacher_id: 老师ID (必填)
    操作:
        调用TMS接口 https://tms.51talk.com/tea_list/do_remark_teacher 重置老师密码
    """
    client = None
    try:
        data = request.json
        teacher_id = data.get('teacher_id')

        if not teacher_id:
            return jsonify({
                'code': '400',
                'msg': '老师ID不能为空',
                'data': None
            }), 400

        logger.info(f"[重置老师密码] 开始处理老师ID: {teacher_id}")

        # 使用 CRMClient 获取 Session
        client = CRMClient()
        session = client.get_session()
        if not session:
            logger.error("[重置老师密码] CRM登录失败,无法获取有效Session")
            return jsonify({
                'code': '500',
                'msg': 'CRM登录失败，无法获取有效Session',
                'data': None
            }), 500

        # 调用TMS接口重置密码
        tms_url = 'https://tms.51talk.com/tea_list/do_remark_teacher'
        params = {
            'content': '1',
            'tea_id': teacher_id,
            'type': '10'
        }

        logger.info(f"[重置老师密码] 调用TMS接口: {tms_url}, 参数: {params}")

        # 使用环境适配方法发送请求 - POST请求使用data参数
        response = get_request_with_host_override(
            session,
            tms_url,
            method='POST',
            data=params,
            timeout=30,
            verify=False
        )

        logger.info(f"[重置老师密码] 响应状态码: {response.status_code}")
        logger.info(f"[重置老师密码] 响应内容: {response.text[:500]}")

        if response.status_code == 200:
            try:
                response_data = response.json()
                logger.info(f"[重置老师密码] 响应数据: {response_data}")

                # 检查接口返回状态 - status 为 1 表示成功
                if response_data.get('status') == 1 or response_data.get('status') == 'success':
                    # 使用固定的成功提示文案
                    success_msg = '密码重置成功，新密码：51talk123456'
                    logger.info(f"[重置老师密码] 成功: {success_msg}")
                    return jsonify({
                        'code': '0',
                        'msg': success_msg,
                        'data': {
                            'teacher_id': teacher_id,
                            'info': success_msg
                        }
                    })
                else:
                    error_msg = response_data.get('info') or response_data.get('msg') or response_data.get('message', '重置密码失败')
                    logger.error(f"[重置老师密码] 接口返回错误: {error_msg}")
                    return jsonify({
                        'code': '500',
                        'msg': f'重置密码失败: {error_msg}',
                        'data': None
                    }), 500
            except Exception as e:
                logger.error(f"[重置老师密码] 解析响应失败: {str(e)}, 响应内容: {response.text[:500]}")
                return jsonify({
                    'code': '500',
                    'msg': f'解析响应失败: {str(e)}',
                    'data': {'raw_response': response.text[:500]}
                }), 500
        else:
            logger.error(f"[重置老师密码] 接口返回错误状态码: {response.status_code}, 响应: {response.text[:200]}")
            return jsonify({
                'code': '500',
                'msg': f'接口调用失败，状态码: {response.status_code}',
                'data': None
            }), 500

    except requests.exceptions.Timeout:
        logger.error("[重置老师密码] TMS接口调用超时")
        return jsonify({
            'code': '500',
            'msg': 'TMS接口调用超时',
            'data': None
        }), 500
    except Exception as e:
        logger.error(f"[重置老师密码] 未知错误: {str(e)}")
        return jsonify({
            'code': '500',
            'msg': f'操作失败: {str(e)}',
            'data': None
        }), 500
    finally:
        if client:
            client.close()


@teacher_bp.route('/get_tms_sso_url', methods=['POST'])
def get_tms_sso_url():
    """
    获取 TMS SSO 跳转 URL
    登录 CRM 后从响应中提取 TMS SSO URL，前端用此 URL 完成浏览器侧的 TMS session 建立
    参数:
        target_url: TMS 目标页面 URL (必填)
    """
    client = None
    try:
        data = request.json
        target_url = data.get('target_url')

        if not target_url:
            return jsonify({'code': '400', 'msg': 'target_url 不能为空', 'data': None}), 400

        logger.info(f"[TMS SSO] 获取 SSO URL，目标页面: {target_url}")

        import hashlib
        session = requests.Session()
        session.verify = False

        md5_pwd = hashlib.md5('51talk20250227#'.encode()).hexdigest()
        resp = session.post(
            'https://crm.51talk.com/admin/login.php',
            data={'user_name': 'admin', 'password': md5_pwd, 'user_type': 'admin', 'login_type': 'tmp'},
            allow_redirects=False,
            timeout=15
        )

        match = re.search(r'window\.location\.href="(//tms\.51talk\.com[^"]+)"', resp.text)
        if not match:
            return jsonify({'code': '500', 'msg': 'CRM 登录失败或未获取到 SSO URL', 'data': None}), 500

        sso_url = 'https:' + match.group(1)
        logger.info(f"[TMS SSO] 获取到 SSO URL: {sso_url[:80]}...")

        return jsonify({
            'code': '0',
            'msg': '获取成功',
            'data': {
                'sso_url': sso_url,
                'target_url': target_url
            }
        })

    except Exception as e:
        logger.error(f"[TMS SSO] 错误: {e}")
        return jsonify({'code': '500', 'msg': f'获取失败: {str(e)}', 'data': None}), 500
