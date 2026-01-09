# 文件: ai_add_point
# 作者: bao0
# 创建日期: 2026/01/08
# 描述: 这是一个给用户添加AI点数的方法
import logging
from common.db_connect import create_connection

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def add_ai_point(connection,  user_id):
    """添加AI点数"""
    add_query ="INSERT INTO `point`.`user_assets` (`stu_id` ,`count`, `sku_id`, `sku_type`, `valid_start`, `valid_end`, `days`) VALUES (%s, 100.00, 113, 'ai_teach', '2025-05-29', '2026-06-27', 300)"

    cursor = connection.cursor()
    try:
        cursor.execute(add_query, user_id)
        logging.info(f"Executed: {add_query} with user_id={user_id}")
        connection.commit()  # 提交事务
    finally:
        cursor.close()


def main():
    """主函数，执行添加AI点数"""
    user_id = 1587398779

    # 创建数据库连接
    connection = create_connection()


    # 添加AI点数
    add_ai_point(connection, user_id)


if __name__ == "__main__":
    main()
