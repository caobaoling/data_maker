# 文件: elf_del_task
# 作者: bao0
# 创建日期: 2024/10/23
# 描述: 这是一个清空用户的新任务的方法-精灵
import logging
from common.db_connect import create_connection, execute_query
from common.execute_batch import execute_batch_op

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_task_ids(connection, user_id):
    """查询需要删除的任务ID"""
    select_query = """select id from talkplatform_task.user_task where user_id = %s and task_info_id in (
        select id from talkplatform_task.task_info where biz_category = 'game_system'  and id >= 20935
    )"""
    return execute_query(connection, select_query, (user_id,))

def main():
    """主函数，执行任务清理"""
    user_id = 1587401009

    # 创建数据库连接
    connection = create_connection()

    # 查询需要删除的任务ID
    task_ids = fetch_task_ids(connection, user_id)

    # 删除与任务相关的所有数据
    for row in task_ids:
        task_id = row[0]
        """删除与任务相关的所有数据"""
        delete_queries = [
            ("delete from talkplatform_task.user_task where id = %s", "id"),
            ("delete from talkplatform_task.user_task_award where id = %s", "id"),
            (f"delete from talkplatform_task.user_task_{int(str(user_id)[-2:])} where id = %s", "id"),
            ("delete from talkplatform_task.user_task_process_record where user_task_id = %s", "user_task_id"),
            ("delete from talkplatform_task.user_award where user_task_id = %s", "user_task_id"),
            (f"delete from talkplatform_task.user_award_{int(str(user_id)[-2:])} where user_task_id = %s",
             "user_task_id")
        ]

        execute_batch_op(connection, delete_queries, task_id)


if __name__ == "__main__":
    main()
#
# import logging
# from common.db_connect import create_connection, execute_query
# from common.execute_delete_batch import execute_delete_batch
#
# # 配置日志
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
#
# def clean_elf_tasks(connection, user_id):
#     # 根据图片修正后缀逻辑：直接取模转字符串，不补零
#     # 例如：1587393646 % 100 = 46 -> "46"
#     # 例如：1000000005 % 100 = 5  -> "5" (对应表 user_task_5)
#     suffix = str(user_id % 100)
#
#     # 1. 查询相关的任务 ID
#     select_sql = """
#         SELECT id FROM talkplatform_task.user_task
#         WHERE user_id = %s AND task_info_id IN (
#             SELECT id FROM talkplatform_task.task_info
#             WHERE biz_category = 'game_system' AND id >= 20935
#         )
#     """
#     rows = execute_query(connection, select_sql, (user_id,))
#     task_ids = [row[0] for row in rows]
#
#     if not task_ids:
#         logging.info(f"用户 {user_id} 没有需要清理的任务记录。")
#         return
#
#     # 2. 准备批量删除的占位符
#     placeholders = ', '.join(['%s'] * len(task_ids))
#     # 3. 构造 SQL 列表 (注意后缀变量 suffix)
#     delete_queries = [
#         f"DELETE FROM talkplatform_task.user_task WHERE id IN ({placeholders})",
#         f"DELETE FROM talkplatform_task.user_task_award WHERE id IN ({placeholders})",
#         f"DELETE FROM talkplatform_task.user_task_{suffix} WHERE id IN ({placeholders})",
#         f"DELETE FROM talkplatform_task.user_task_process_record WHERE user_task_id IN ({placeholders})",
#         f"DELETE FROM talkplatform_task.user_award WHERE user_task_id IN ({placeholders})",
#         f"DELETE FROM talkplatform_task.user_award_{suffix} WHERE user_task_id IN ({placeholders})"
#     ]
#
#     # 4. 调用通用的执行器，传入 task_ids 的元组
#     execute_delete_batch(connection, delete_queries, tuple(task_ids))
#
#
# def main():
#     user_id = 1587393646
#     connection = create_connection()
#     try:
#         clean_elf_tasks(connection, user_id)
#     finally:
#         connection.close()
#
#
# if __name__ == "__main__":
#     main()