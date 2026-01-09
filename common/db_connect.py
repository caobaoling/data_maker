# 文件: db_connect
# 作者: bao0
# 创建日期: 2024/10/23
# 描述: 这是一个链接数据库的配置文件

from common.db_utils import load_config
import pymysql


def create_connection():
    """创建数据库连接"""
    config = load_config()
    host = config['host']
    port = config['port']
    user = config['user']
    password = config['password']

    # 使用配置信息连接到 MySQL 数据库
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
    )
    return connection


def close_connection(connection, cursor):
    """关闭数据库连接和游标"""
    cursor.close()
    connection.close()


def execute_query(connection, query, params=None):
    """执行查询并返回结果"""
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


def execute_non_query(connection, query, params=None):
    """执行非查询语句（如插入、更新、删除）"""
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()


def insert_data(connection, table, data):
    """插入数据"""
    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    execute_non_query(connection, query, tuple(data.values()))


def update_data(connection, table, data, condition):
    """更新数据"""
    set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
    params = list(data.values()) + [condition.split('=')[1].strip()]
    execute_non_query(connection, query, params)


def delete_data(connection, table, condition):
    """删除数据"""
    query = f"DELETE FROM {table} WHERE {condition}"
    execute_non_query(connection, query)


def select_data(connection, table, columns='*', condition=None):
    """查询数据"""
    if condition:
        query = f"SELECT {columns} FROM {table} WHERE {condition}"
    else:
        query = f"SELECT {columns} FROM {table}"
    return execute_query(connection, query)

# 示例用法
# if __name__ == "__main__":
#     conn = connect_to_mysql()
#     print("Connected to MySQL database!")
#     conn.close()
