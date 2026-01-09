# 文件: pb_del_data.py
# 作者: bao0
# 创建日期: 2026/01/08
# 描述: 这是一个删除绘本数据的方法
import logging
from common.db_connect import create_connection
from common.execute_batch import execute_batch_op

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """主函数，执行任务清理"""
    user_id = 58153803

    """删除绘本的所有数据"""
    delete_queries = [
        ("DELETE FROM `talkplatform_ai_pbook`.`user_info` WHERE id = %s ", "id"),
        (f"DELETE FROM `talkplatform_ai_pbook`.`user_settlement_{int(str(user_id)[-2:])}` WHERE `stu_id` =  %s",
         "stu_id"),
        ("DELETE FROM `talkplatform_ai_pbook`.`user_weekly_statistics` WHERE `stu_id` =  %s", "stu_id"),
        ("DELETE FROM `talkplatform_ai_pbook`.`course_package_reading_plan` WHERE  `stu_id` =   %s", "stu_id"),
        ("DELETE FROM `talkplatform_ai_pbook`.`weekly_report` WHERE  `stu_id` =   %s", "stu_id"),
        (f"DELETE FROM `talkplatform_ai_pbook`.`user_report_{int(str(user_id)[-2:])}`  WHERE  `stu_id` =%s", "stu_id"),
        (f"DELETE FROM `talkplatform_ai_pbook`.`user_practice_{int(str(user_id)[-2:])}` WHERE  `stu_id` =%s", "stu_id"),
        (f"DELETE FROM `talkplatform_ai_pbook`.`user_game_asset_record_{int(str(user_id)[-2:])}`  WHERE  `stu_id` =%s",
         "stu_id"),
        (f"DELETE FROM  `talkplatform_ai_pbook`.`picture_book_reading_plan_{int(str(user_id)[-2:])}`   WHERE  `stu_id` =%s",
         "stu_id"),
        ("DELETE FROM  `talkplatform_ai_pbook`.`user_daily_statistics_info`  WHERE  `stu_id` =%s", "stu_id"),
        ("DELETE FROM  `talkplatform_ai_pbook`.`picture_book_reading_plan_3`   WHERE  `stu_id` = %s", "stu_id"),
        ("DELETE FROM  `talkplatform_ai_pbook`.`reading_setting` WHERE  `stu_id` = %s", "stu_id")
    ]
    conn = create_connection()
    execute_batch_op(conn, delete_queries, user_id)
    conn.close()


if __name__ == "__main__":
    main()
