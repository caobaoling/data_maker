# 文件: execute_delete_batch
# 作者: bao0
# 创建日期: 2026/01/09
# 描述: 这是一个批量操作数据的文件
import logging


def execute_batch_op(connection, queries, param_value):
    """
    通用的批量执行器
    :param connection: 数据库连接对象
    :param queries: SQL 语句列表
    :param param_value: 需要传入的参数值 (如 user_id 或 time_key)
    """
    cursor = connection.cursor()
    try:
        logging.info(f"开始为 {param_value} 执行批量操作...")
        for query, param_name in queries:
            if "%s" in query:
                # 只有带 %s 的 SQL 才传入参数
                cursor.execute(query, (param_value,))
            else:
                # 不带占位符的 SQL 直接执行（如全局 UPDATE）
                cursor.execute(query)
            # 只记录 SQL 的前 60 个字符，避免日志刷屏
            logging.info(f"成功执行: {query.strip()[:60]}...")
        connection.commit()
        logging.info("所有操作已成功提交。")
    except Exception as e:
        connection.rollback()
        logging.error(f"操作失败，已回滚。错误信息: {e}")
        raise e
    finally:
        cursor.close()
