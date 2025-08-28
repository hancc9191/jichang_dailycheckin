import requests
import os

# 环境变量
SCKEY = os.environ.get('SCKEY')
Token = os.environ.get('TOKEN')

# 多账号（EMAIL 与 PASSWD 用 | 分隔）
emails = os.environ.get('EMAIL').split('|')
passwds = os.environ.get('PASSWD').split('|')

def push(content):
    """统一推送"""
    if SCKEY and SCKEY != '1':
        url = f"https://sctapi.ftqq.com/{SCKEY}.send"
        data = {"title": "ikuuu签到", "desp": content}
        requests.post(url, data=data)
        print('✅ Server酱推送完成')
    elif Token and Token != '1':
        headers = {'Content-Type': 'application/json'}
        data = {"token": Token, 'title': 'ikuuu签到', 'content': content, "template": "json"}
        resp = requests.post('http://www.pushplus.plus/send', json=data, headers=headers).json()
        print('✅ push+推送成功' if resp.get('code') == 200 else '❌ push+推送失败')
    else:
        print('⚠️ 未使用消息推送！')

# ikuuu 新域名
base_url = 'https://ikuuu.de'
login_url = f'{base_url}/auth/login'
check_url = f'{base_url}/user/checkin'

header = {
    'origin': base_url,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

# 存储所有结果
results = []

for i, (email, passwd) in enumerate(zip(emails, passwds), start=1):
    session = requests.Session()  # 每个账号独立 session
    try:
        # 登录
        login_data = {'email': email, 'passwd': passwd}
        resp = session.post(login_url, headers=header, data=login_data).json()
        login_msg = resp.get('msg', '登录失败')
        print(f'账号{i}登录: {login_msg}')

        # 签到
        resp = session.post(check_url, headers=header).json()
        check_msg = resp.get('msg', '签到失败')
        print(f'账号{i}签到: {check_msg}')

        results.append(f'账号{i}（{email}）: {check_msg}')
    except Exception as e:
        results.append(f'账号{i}（{email}）: 出错 - {e}')

# 🚀 循环全部完成后统一推送一次
final_content = '\n'.join(results)
push(final_content)
