"""
用requests模块发送form表单的数据
"""

import requests

login_url = 'http://127.0.0.1'
login_data = {
    "username": "xxx",
    "password": "xxx",
}
s = requests.session() # 登录之后拿到session来进行后续的操作
res = s.post(login_url, json=login_data)

create_team_url = 'http://127.0.0.1'
create_team_form_data = {
    "name": (None, "test1111"),
    # 不是文件流的话，元组中的第一个元素为None
    "logo": ("11.png", open('/home/ywm/Downloads/gif/11.png', 'rb'), "image/png"),
    # 如果是文件流的话， 元组中的第一个元素为文件名，字典的key是变量名
    "brief_introduction": (None, "这是战队的介绍")
}

resp = s.post(create_team_url, files=create_team_form_data)
print(resp.json())
