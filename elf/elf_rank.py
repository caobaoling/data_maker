# 文件: elf_rank
# 作者: bao0
# 创建日期: 2024/10/23
# 描述: 这是一个给精灵排行榜开榜前造数据的方法
# 1. 删除数据库中本周的数据
# 2. 将用户数据设置为可用状态
import logging

from datetime import datetime
import datetime

from common.db_connect import create_connection
from common.execute_batch import execute_batch_op

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_last_sunday_of_previous_week():
    # 获取当前日期
    today = datetime.date.today()

    # 计算当前周的周日日期
    days_to_sunday = 7 - today.isoweekday()
    if days_to_sunday == 7:
        days_to_sunday = 0  # 如果今天就是周日，不需要加天数
    current_sunday = today + datetime.timedelta(days=days_to_sunday)

    # 计算上一周的周日日期
    last_sunday = current_sunday - datetime.timedelta(days=7)

    # 格式化输出为 YYYY-WWW 格式
    formatted_last_sunday = last_sunday.strftime("%Y-w%V")

    return formatted_last_sunday


# 调用函数并打印结果
# print(get_last_sunday_of_previous_week())
formatted_last_sunday = get_last_sunday_of_previous_week()


# formatted_last_sunday = "2025-w09"
print(formatted_last_sunday)


def delete_rank_data(connection, time_key):
    """删除当前周排行榜的所有数据"""
    delete_queries = [
        ("DELETE from talkplatform_game.user_rank_round where time_key =%s", "time_key"),
        ("DELETE from talkplatform_game.rank_round where time_key =%s", "time_key"),
        ("DELETE from talkplatform_game.rank_round_reward where time_key = %s", "time_key")
    ]

    conn = create_connection()
    execute_batch_op(conn, delete_queries, time_key)
    conn.close()


def update_rank_data(connection, user_id):
    """更新当前周排行榜的所有数据"""
    # 更新机器人的使用状态

    # 更新用户的使用状态

    update_queries = [
        ("UPDATE talkplatform_game.robot_rank set use_status=0;", "none"),
        ("UPDATE `talkplatform_game`.`user_rank_level` SET`use_flag` = 0, `del_flag` = 0 ;", "none")
    ]

    conn = create_connection()
    execute_batch_op( conn, update_queries, user_id)
    conn.close()


def main():
    # 创建数据库连接
    connection = create_connection()
    # # 打印时间键值
    # print(f"Formatted last Sunday: {formatted_last_sunday}")

    # 删除排行榜数据
    delete_rank_data(connection, formatted_last_sunday)
    update_rank_data(connection, "none")


if __name__ == "__main__":
    main()
