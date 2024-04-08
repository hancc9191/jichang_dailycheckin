import requests
import json
import os

session = requests.session()

# 配置用户名和密码（一般是邮箱）
email1 = os.environ.get('EMAIL1')
passwd1 = os.environ.get('PASSWD1')

email2 = os.environ.get('EMAIL')
passwd2 = os.environ.get('PASSWD')

# server酱
SCKEY = os.environ.get('SCKEY')
# PUSHPLUS
Token = os.environ.get('TOKEN')

def push(content):
    if SCKEY != '1':
        url = "https://sctapi.ftqq.com/{}.send?title={}&desp={}".format(SCKEY, 'ikuuu签到', content)
        requests.post(url)
        print('推送完成')
    elif Token != '1':
        headers = {'Content-Type': 'application/json'}
        json = {"token": Token, 'title': 'ikuuu签到', 'content': content, "template": "json"}
        resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
        print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')
    else:
        print('未使用消息推送推送！')

def login_and_checkin(email, passwd):
    try:
        print(f'进行账号 {email} 的登录...')
        login_url = 'https://ikuuu.pw/auth/login'
        check_url = 'https://ikuuu.pw/user/checkin'
        info_url = 'https://ikuuu.pw/user/profile'

        header = {
            'origin': 'https://ikuuu.me',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        data = {
            'email': email,
            'passwd': passwd
        }

        # 登录
        response = session.post(url=login_url, headers=header, data=data).json()
        print(response['msg'])

        # 获取账号名称
        info_html = session.get(url=info_url, headers=header).text
        info = "".join(re.findall('<span class="user-name text-bold-600">(.*?)</span>', info_html, re.S))
        print(info)

        # 进行签到
        result = session.post(url=check_url, headers=header).json()
        print(result['msg'])
        content = result['msg']

        return content

    except Exception as e:
        print(f'账号 {email} 签到失败')
        print(str(e))
        raise

try:
    contents = []
    contents.append(login_and_checkin(email, passwd))
    contents.append(login_and_checkin(email1, passwd1))
    push("\n".join(contents))
except Exception as e:
    content = '签到失败'
    print(content)
    push(content)
