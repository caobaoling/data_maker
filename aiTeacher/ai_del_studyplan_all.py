# 文件: ai_del_studyplan_all.py
# 作者: bao0
# 创建日期: 2026/01/08
# 描述: 这是一个清空用户所有学习计划的方法
import logging
from common.db_connect import create_connection
from common.execute_batch import execute_batch_op

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """主函数，执行学习计划清理"""
    user_id = 800018551

    """删除与学习计划相关的所有数据"""
    delete_queries = [
        ("DELETE FROM `talkplatform_ai_teacher`.`user_info` WHERE user_info.id=%s", "id"),
        ("DELETE FROM `talkplatform_ai_teacher`.`user_lesson_consume_record` WHERE user_lesson_consume_record.user_id=%s",
         "id"),
        ("DELETE FROM `talkplatform_ai_teacher`.`user_lesson_exam_info` WHERE user_lesson_exam_info.user_id=%s", "id"),
        ("DELETE FROM `talkplatform_ai_teacher`.`user_report` WHERE user_report.user_id= %s", "user_id"),
        ("DELETE FROM `talkplatform_ai_teacher`.`user_test_analysis` WHERE user_test_analysis.user_id= %s", "user_id"),
        ("DELETE FROM `talkplatform_ai_teacher`.`user_statistics_gold_coin_log` WHERE user_statistics_gold_coin_log.user_id= %s",
         "user_id"),
        ("DELETE FROM `talkplatform_ai_teacher`.`user_week_statistics` WHERE user_week_statistics.user_id= %s",
         "user_id"),
        ("DELETE FROM `talkplatform_ai_teacher`.`user_week_plan` WHERE user_week_plan.user_id=%s", "user_id"),
        ("DELETE FROM `talkplatform_ai_teacher`.`user_timetable_finish_record` WHERE user_timetable_finish_record.user_id=%s",
         "user_id"),
        ("DELETE FROM `talkplatform_ai_teacher`.`user_statistics` WHERE user_statistics.user_id= %s", "user_id"),
        ("DELETE FROM `talkplatform_ai_teacher`.`user_timetable` WHERE user_timetable.user_id= %s", "user_id"),
        ("DELETE FROM `talkplatform_ai_teacher`.`user_update_log` WHERE user_update_log.user_id= %s", "user_id")
    ]

    conn = create_connection()
    execute_batch_op(conn, delete_queries, user_id)
    conn.close()


if __name__ == "__main__":
    main()
