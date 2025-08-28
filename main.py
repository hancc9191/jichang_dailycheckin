import requests
import json
import os

session = requests.session()

# Retrieve environment variables
SCKEY = os.environ.get('SCKEY')
Token = os.environ.get('TOKEN')

# 多账号信息（邮箱和密码以 | 分隔）
emails = os.environ.get('EMAIL').split('|')
passwds = os.environ.get('PASSWD').split('|')

def push(content):
    if SCKEY and SCKEY != '1':
        url = f"https://sctapi.ftqq.com/{SCKEY}.send?title=ikuuu签到&desp={content}"
        requests.post(url)
        print('Server酱推送完成')
    elif Token and Token != '1':
        headers = {'Content-Type': 'application/json'}
        data = {"token": Token, 'title': 'ikuuu签到', 'content': content, "template": "json"}
        resp = requests.post('http://www.pushplus.plus/send', json=data, headers=headers).json()
        print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')
    else:
        print('未使用消息推送！')

login_url = 'https://ikuuu.de/auth/login'
check_url = 'https://ikuuu.de/user/checkin'
info_url = 'https://ikuuu.de/user/profile'

header = {
    'origin': 'https://ikuuu.de',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

# 初始化结果
results = []

# 多账号循环
for i, (email, passwd) in enumerate(zip(emails, passwds), start=1):
    try:
        print(f'账号{i} - {email} 开始登录...')
        login_data = {'email': email, 'passwd': passwd}
        response = session.post(url=login_url, headers=header, data=login_data).json()
        msg = response.get('msg', '登录失败')
        print(f'账号{i}登录结果: {msg}')

        # 签到
        result = session.post(url=check_url, headers=header).json()
        check_msg = result.get('msg', '签到失败')
        print(f'账号{i}签到结果: {check_msg}')

        results.append(f'账号{i}（{email}）: {check_msg}')
    except Exception as e:
        error_msg = f'账号{i}（{email}）签到失败: {e}'
        print(error_msg)
        results.append(error_msg)

# 所有账号签到完成后统一推送
content = '\n'.join(results)
push(content)
