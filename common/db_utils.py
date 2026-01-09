# 文件: db_utils.py
# 作者: bao0
# 创建日期: 2024/12/3
# 描述: 这是一个读取配置的文件
import json
import os


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '../config', 'database.json')
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config
