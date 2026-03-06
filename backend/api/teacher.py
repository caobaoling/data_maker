# 文件: api/teacher.py
# 作者: Claude Code
# 创建日期: 2026/03/06
# 描述: 外教管理工具API

from flask import Blueprint, request, jsonify
import sys
import os
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录以导入common模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from common.db_connect import create_connection
from common.tms_client import get_tms_session

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

def get_tms_session():
    """
    获取TMS Session (通过表单登录)
    返回: requests.Session对象
    """
    session = requests.Session()

    try:
        login_url = 'https://tms.51talk.com/admin/login.php'
        password_md5 = hashlib.md5('51talk20250227#'.encode()).hexdigest()

        credentials = {
            'user_name': 'admin',
            'password': password_md5,
            'ref': '',
            'user_type': 'admin',
            'login_type': 'tmp'
        }

        logger.info(f"[TMS登录] 正在登录TMS系统...")

        response = session.post(
            login_url,
            data=credentials,
            verify=False,
            allow_redirects=True,
            timeout=30
        )

        if response.status_code == 200:
            cookies = session.cookies.get_dict()
            admin_code = cookies.get('admin_code')

            if admin_code:
                logger.info(f"[TMS登录] 登录成功")
                return session
            else:
                logger.error(f"[TMS登录] 登录失败,未获取到admin_code")
                return None
        else:
            logger.error(f"[TMS登录] 登录失败,状态码: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"[TMS登录] 登录异常: {e}")
        return None

def update_tms_sa_end_time(teacher_id):
    """
    步骤2: 调用TMS接口更新sa_end_time
    返回: (是否成功, 日志消息, sa_end_time值)
    """
    try:
        # 计算当前时间+2年
        sa_end_time = (datetime.now() + relativedelta(years=2)).strftime('%Y-%m-%d 23:59:59')

        # 自动登录获取Session
        session = get_tms_session()
        if not session:
            log_msg = "TMS登录失败,无法获取有效Session"
            logger.error(f"[步骤2-TMS接口] {log_msg}")
            return (False, log_msg, sa_end_time)

        tms_url = 'https://tms.51talk.com/tea_promotion/batchUpdateTeacherInfo'
        params = {
            't_ids': teacher_id,
            'field': 'sa_end_time',
            'value': sa_end_time,
            'do': '1'
        }

        logger.info(f"[步骤2-TMS接口] 调用接口更新sa_end_time")

        response = session.get(
            tms_url,
            params=params,
            timeout=30,
            verify=False  # 忽略SSL证书验证
        )

        logger.info(f"[步骤2-TMS接口] 响应状态码: {response.status_code}, 响应内容: {response.text[:500]}")

        if response.status_code == 200:
            response_text = response.text.strip()

            # 优先检查权限错误
            if 'no permission' in response_text.lower():
                log_msg = f"TMS接口权限不足: {response_text}"
                logger.error(f"[步骤2-TMS接口] {log_msg}")
                return (False, log_msg, sa_end_time)

            # 检查是否包含xdebug调试信息(说明接口调用成功,只是返回了调试信息)
            if 'xdebug-var-dump' in response_text and str(teacher_id) in response_text:
                log_msg = f"成功更新TMS，老师ID: {teacher_id}, sa_end_time: {sa_end_time} (接口返回调试信息)"
                logger.info(f"[步骤2-TMS接口] {log_msg}")
                return (True, log_msg, sa_end_time)

            # 尝试解析JSON响应
            try:
                response_data = response.json()
                # 检查TMS接口返回的业务状态
                if response_data.get('status') == 1 or response_data.get('code') == 0:
                    log_msg = f"成功更新TMS，老师ID: {teacher_id}, sa_end_time: {sa_end_time}"
                    logger.info(f"[步骤2-TMS接口] {log_msg}")
                    return (True, log_msg, sa_end_time)
                else:
                    log_msg = f"TMS接口返回业务错误: {response_data.get('msg', '未知错误')}"
                    logger.error(f"[步骤2-TMS接口] {log_msg}, 完整响应: {response.text}")
                    return (False, log_msg, sa_end_time)
            except Exception as json_error:
                # 如果不是JSON格式,检查是否包含成功标识
                if 'success' in response_text.lower() or 'ok' in response_text.lower():
                    log_msg = f"成功更新TMS，老师ID: {teacher_id}, sa_end_time: {sa_end_time}"
                    logger.info(f"[步骤2-TMS接口] {log_msg}")
                    return (True, log_msg, sa_end_time)
                else:
                    log_msg = f"TMS接口返回非预期响应: {response_text[:200]}"
                    logger.error(f"[步骤2-TMS接口] {log_msg}")
                    return (False, log_msg, sa_end_time)
        else:
            log_msg = f"TMS接口返回错误状态码: {response.status_code}, 响应: {response.text[:200]}"
            logger.error(f"[步骤2-TMS接口] {log_msg}")
            return (False, log_msg, sa_end_time)

    except requests.exceptions.Timeout:
        log_msg = "TMS接口调用超时"
        logger.error(f"[步骤2-TMS接口] {log_msg}")
        return (False, log_msg, None)
    except Exception as e:
        log_msg = f"TMS接口调用失败: {str(e)}"
        logger.error(f"[步骤2-TMS接口] {log_msg}")
        return (False, log_msg, None)

@teacher_bp.route('/add_pre_contract', methods=['POST'])
def add_pre_contract():
    """
    为老师添加合同(SA)
    参数:
        teacher_id: 老师ID (必填)
    操作:
        1. 插入数据库记录到 talk.teacher_contract
        2. 调用TMS接口更新sa_end_time
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

        # 步骤2: 调用TMS接口
        tms_success, tms_log, sa_end_time = update_tms_sa_end_time(teacher_id)
        result['steps'].append({
            'step': 2,
            'name': 'TMS接口调用',
            'success': tms_success,
            'log': tms_log,
            'sa_end_time': sa_end_time
        })

        # 判断整体成功: TMS成功即为成功(即使DB跳过插入)
        result['success'] = tms_success
        result['db_insert'] = db_success
        result['tms_update'] = tms_success

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
