# 文件: url_unquote
# 作者: bao0
# 创建日期: 2024/10/21
# 描述: 这是一个转码工具
from urllib.parse import unquote
"""

"""
# 使用 unquote 函数
url = "https://appkidi.51suyang.cn/User/userAutoLogin?link=https%3A%2F%2Fresources.51suyang.cn%2FPictureBook%2FApi%2FPictureBook%2FlistHtml%3Ftoken%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNTgwMjQyNDUifQ.AHn7noRvae9G7Z4-E1PnwbH50vzzJ1N94akZBQ2DqhU%26version%3D6.4.0%26systemVer%3D14.2%26device_firm%3DApple%26resource_domain%3Dresources.51suyang.cn"
decoded_url = unquote(url)
print(decoded_url)