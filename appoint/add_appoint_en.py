# 文件: add_appoint
# 作者: bao0
# 创建日期: 2024/10/23
# 描述: 这是一个预约课程的方法
import requests
import time
import random

from datetime import datetime, timedelta
# 定义 API URL
url = 'http://172.16.16.97/talkplatform_appointone_consumer/v1/appoint/add'

t_id = 2821   # 普通话老师=350012781，外教老师=2821
stu_id = 1587397944
start_time = "2025-12-10 18:30:00"
status = "on"   #on的状态
course_type = "1"  #1v1英语课=1，普通话=31
point_type = "point"    #1v1英语课=point，普通话=pthpoint
# # 付费课教材
# use_point = "buy"    #付费课
# course_id = "1166431"
# course_top_id = "1161041"
# course_sub_id = "1163731"
# # 付费课教材-H5 L1-U17-L8
# use_point = "buy"    #付费课
# course_id = "777831"
# course_top_id = "769941"
# course_sub_id = "772121"
# # 付费课教材-H5 L0-U1-L1
# use_point = "buy"    #付费课
# course_id = "793091"
# course_top_id = "773011"
# course_sub_id = "793011"
# 付费课教材-H5 L0-U18-L8
use_point = "buy"    #付费课
course_id = "776441"
course_top_id = "773011"
course_sub_id = "770201"
# # # 付费课教材-商务英语
# use_point = "buy"    #付费课
# course_id = "7775"
# course_top_id = "24"
# course_sub_id = "7764"

# # 体验课教材
# use_point = "free"    #体验课
# course_id = "821221"
# course_top_id = "822151"
# course_sub_id = "820171"
#查看教材id https://om.51talk.com/textbook/seriesbook/index?course_type=1&teach_type=v2&parent=8595&status=&course_id=&stu_book_prefix=&stu_path=&textbook_type=v2
# 提取end_time
start_s = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
end_time_e = start_s + timedelta(minutes=30)
end_time = end_time_e.strftime('%Y-%m-%d %H:%M:%S')
# print(end_time)
category = "ph_"+use_point
# 提取小时和分钟
dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

hour = dt.hour
minute = dt.minute

# 计算下划线后面的数字
suffix = hour * 2 + 1
if minute == 30:
    suffix += 1

# 生成最终的格式化字符串
date_time = f"{dt.strftime('%Y%m%d')}_{suffix}"
date = f"{dt.strftime('%Y%m%d')}"
time = suffix
# 输出结果
# print(date_time)
# print(date)
# print(time)

current_time = datetime.now()

# 格式化时间为指定格式
add_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

# 生成 1 到 10 位的随机数
def generate_random_number(min_length=1, max_length=10):
    # 生成一个随机长度
    length = random.randint(min_length, max_length)

    # 生成一个指定长度的随机数
    random_number = random.randint(10 ** (length - 1), 10 ** length - 1)

    return random_number


# 调用函数生成随机数
random_number = generate_random_number()
# print(random_number)

# 定义查询参数
data = {
    "id": random.randint(171605105, 971605105),
    "t_id": t_id,
    "s_id": stu_id,
    "tag_id": "87703151451772984942",
    "start_time": start_time,
    "end_time": end_time,
    "date_time": date_time,
    "status": status,
    "date": date,
    "time": time,
    "week": "0",
    "add_time": add_time,
    "course_id": course_id,
    "now_level": "0",
    "appoint_type": "ios",
    "point_type": point_type,
    "cost_num": "1",
    "teach_type": "51TalkAC",
    "use_point": use_point,
    "cancel_operator": "0",
    "use_skype_id": "0",
    "need_oral": "0",
    "course_top_id": course_top_id,
    "course_sub_id": course_sub_id,
    "course_type": course_type,
    "tea_salary": "0",
    "package_id": "0",
    "category": category
}
# 定义自定义头部
headers = {
    'Authorization': 'Bearer your_token',
    'Content-Type': 'application/json'
}
# 发送 POST 请求
response = requests.post(url, json=data, headers=headers)
# 检查请求是否成功
if response.status_code == 200:
    # 解析响应内容
    data = response.json()  # 假设响应内容是 JSON 格式
    print(data)
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

