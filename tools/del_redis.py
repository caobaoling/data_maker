# 文件: del_redis
# 作者: bao0
# 创建日期: 2025/4/2
# 描述: 这是一个删除redis缓存的文件
# 安装redis-py库（若未安装）
#
import redis


# 创建Redis连接
def connect_redis(host, port, db):
    try:
        # 创建连接对象
        r = redis.Redis(
            host=host,
            port=port,
            db=db  # 自动解码返回字符串
        )

        # 测试连接是否成功
        if r.ping():
            # print("Successfully connected to Redis")
            return r
    except redis.ConnectionError as e:
        print(f"Connection failed: {e}")
    return None


def scan_keys(redis_client, pattern, batch_size=100):
    cursor = '0'
    found_keys = []
    while cursor != 0:
        cursor, keys = redis_client.scan(
            cursor=cursor,
            match=pattern,
            count=batch_size
        )
        found_keys.extend(keys)
    return found_keys


# 使用示例
if __name__ == "__main__":
    host = '172.16.70.21'
    port = '6379'
    db = 0
    for port in port.split(','):

        redis_client = connect_redis(host, port, db)
        redis_key = '1587398158'

        # 基本操作示例
        if redis_client:
            pattern = '*' + redis_key + '*'
            result = scan_keys(redis_client, pattern)
            if result:
                try:
                    print(f"Scan found {len(result)} keys:")

                    # 批量删除操作
                    deleted_count = redis_client.delete(*result)
                    print(f"Successfully deleted {deleted_count} keys matching pattern: {pattern}")
                    print('\n'.join(result))
                except redis.RedisError as e:
                    print(f"Delete operation failed: {str(e)}")
            else:
                print("No keys found matching the pattern")
