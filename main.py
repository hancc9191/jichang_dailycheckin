import requests
import os
import re

SCKEY = os.environ.get('SCKEY')
Token = os.environ.get('TOKEN')

emails = os.environ.get('EMAIL', '').split('|')
passwds = os.environ.get('PASSWD', '').split('|')

def push(content):
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

BASE_URL = 'https://ikuuu.de'
LOGIN_URL = f'{BASE_URL}/auth/login'
CHECKIN_URL = f'{BASE_URL}/user/checkin'
PROFILE_URL = f'{BASE_URL}/user/profile'
USER_URL = f'{BASE_URL}/user'

HEADERS = {
    'origin': BASE_URL,
    'referer': f'{BASE_URL}/auth/login',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

results = []

def format_traffic(bytes_value):
    """将字节数格式化成 MB / GB"""
    if bytes_value < 1024**2:
        return f"{bytes_value} B"
    elif bytes_value < 1024**3:
        return f"{bytes_value/1024/1024:.2f} MB"
    else:
        return f"{bytes_value/1024/1024/1024:.2f} GB"

for i, (email, passwd) in enumerate(zip(emails, passwds), start=1):
    session = requests.Session()
    try:
        # 登录
        login_data = {'email': email, 'passwd': passwd}
        resp = session.post(LOGIN_URL, headers=HEADERS, data=login_data, timeout=10).json()
        login_msg = resp.get('msg', '登录失败')
        print(f'账号{i}登录: {login_msg}')

        # 签到
        resp = session.post(CHECKIN_URL, headers=HEADERS, timeout=10).json()
        check_msg = resp.get('msg', '签到失败')
        print(f'账号{i}签到: {check_msg}')

        # 先试 /user/profile JSON API
        transfer, expire = "未知", "未知"
        try:
            profile = session.get(PROFILE_URL, headers=HEADERS, timeout=10).json()
            transfer_enable = profile.get('transfer_enable')
            u = profile.get('u')
            d = profile.get('d')
            expire = profile.get('class_expire', '未知')

            if transfer_enable:
                used = (u or 0) + (d or 0)
                left = transfer_enable - used
                transfer = format_traffic(left)
        except Exception:
            # 如果 JSON 失败，再尝试 HTML
            html = session.get(USER_URL, headers=HEADERS, timeout=10).text
            transfer_match = re.search(r'(\d+\.?\d*\s*(?:GB|MB))', html)
            expire_match = re.search(r'(\d{4}-\d{2}-\d{2})', html)
            transfer = transfer_match.group(1) if transfer_match else "未知"
            expire = expire_match.group(1) if expire_match else "未知"

        results.append(
            f"账号{i}（{email}）\n"
            f"签到: {check_msg}\n"
            f"剩余流量: {transfer}\n"
            f"到期时间: {expire}\n"
            "-------------------------"
        )

    except Exception as e:
        results.append(f"账号{i}（{email}）: 出错 - {e}\n-------------------------")

final_content = "\n".join(results)
print("推送内容:\n", final_content)
push(final_content)
