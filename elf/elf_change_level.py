# 文件: elf_change_level
# 作者: bao0
# 创建日期: 2024/11/28
# 描述: 这是一个给精灵变更级别的方法
import logging
from common.db_connect import create_connection, execute_query
from common.elf_level_config import ElfLevelData

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def update_elf_level(connection, user_id, elf_total_exp, elf_level_exp, elf_level, elf_style_code):
    """更新精灵的级别"""
    """更新用户精灵的经验和等级"""

    update_query = """
        UPDATE `talkplatform_game`.`user_elf` 
        SET `elf_total_exp` = %s, 
            `elf_level_exp` = %s, 
            `elf_level` = %s, 
            `elf_style_code` = %s 
        WHERE user_id = %s;
        """
    try:
        with connection.cursor() as cursor:
            cursor.execute(update_query, (elf_total_exp, elf_level_exp, elf_level, elf_style_code, user_id))
            connection.commit()  # 提交事务
            logging.info(f"Updated user_elf for user_id={user_id}")
    except Exception as e:
        connection.rollback()  # 回滚事务
        logging.error(f"Error updating user_elf for user_id={user_id}: {e}")
    finally:
        cursor.close()


def main():
    """主函数，执行任务清理"""
    connection = create_connection()
    user_id = 1587397947
    level = 8
    level_data = ElfLevelData.get_level_data(level)
    print(level_data['elf_total_exp'])
    update_elf_level(connection, user_id, level_data['elf_total_exp'], level_data['elf_level_exp'], level,
                     level_data['elf_style_code'])

    if level_data:
        print(f"Level {level} data: {level_data}")
    else:
        print(f"No data found for level {level}")


if __name__ == "__main__":
    main()
