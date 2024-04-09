import requests
import json
import re
import os

session = requests.session()

# Retrieve environment variables
email = os.environ.get('EMAIL')
passwd = os.environ.get('PASSWD')
SCKEY = os.environ.get('SCKEY')
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

# Initialize an empty list to store messages
results = []

try:
    print('进行登录...')
    response = json.loads(session.post(url=login_url, headers=header, data=data).text)
    print(response['msg'])
    
    # Get user info
    info_html = session.get(url=info_url, headers=header).text
    # info = "".join(re.findall('<span class="user-name text-bold-600">(.*?)</span>', info_html, re.S))
    # print(info)
    
    # Check in
    result = json.loads(session.post(url=check_url, headers=header).text)
    print(result['msg'])
    results.append(result['msg'])  # Append the check-in result message
    
except Exception as e:
    error_msg = '签到失败: ' + str(e)
    print(error_msg)
    results.append(error_msg)  # Append the error message

# Combine all messages into a single string
content = '\n'.join(results)

# Send a unified push notification
push(content)
