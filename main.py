import requests
import os

# -------------------------------
# 配置推送
# -------------------------------
SCKEY = os.environ.get('SCKEY')
Token = os.environ.get('TOKEN')

# -------------------------------
# 多账号设置
# EMAIL 和 PASSWD 用 | 分隔
# -------------------------------
emails = os.environ.get('EMAIL', '').split('|')
passwds = os.environ.get('PASSWD', '').split('|')

# -------------------------------
# 推送函数
# -------------------------------
def push(content):
    title = 'ikuuu签到'
    # 优先 Server酱（新接口）
    if SCKEY and SCKEY != '1':
        try:
            url = f"https://sctapi.ftqq.com/{SCKEY}.send"
            data = {"title": title, "desp": content}
            requests.post(url, data=data, timeout=10)
            print('推送完成（Server酱）')
        except Exception as e:
            print(f'Server酱推送失败：{e}')
    # 其次 Push+
    elif Token and Token != '1':
        try:
            url = "https://www.pushplus.plus/send"  # 修正为 https
            headers = {'Content-Type': 'application/json'}
            payload = {"token": Token, "title": title, "content": content, "template": "json"}
            resp = requests.post(url, json=payload, headers=headers, timeout=10).json()
            print('push+推送成功' if resp.get('code') == 200 else f'push+推送失败：{resp}')
        except Exception as e:
            print(f'push+推送异常：{e}')
    else:
        print('未使用消息推送！')

# -------------------------------
# ikuuu 域名和接口
# -------------------------------
BASE_URL = 'https://ikuuu.de'
LOGIN_URL = f'{BASE_URL}/auth/login'
CHECKIN_URL = f'{BASE_URL}/user/checkin'
USERINFO_URL = f'{BASE_URL}/getuserinfo'

HEADERS = {
    'origin': BASE_URL,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# -------------------------------
# 存储所有账号签到结果
# -------------------------------
results = []

for i, (email, passwd) in enumerate(zip(emails, passwds), start=1):
    session = requests.Session()
    try:
        # 登录
        login_data = {'email': email, 'passwd': passwd}
        resp = session.post(LOGIN_URL, headers=HEADERS, data=login_data).json()
        login_msg = resp.get('msg', '登录失败')
        print(f'账号{i}登录: {login_msg}')

        # 签到
        resp = session.post(CHECKIN_URL, headers=HEADERS).json()
        check_msg = resp.get('msg', '签到失败')
        print(f'账号{i}签到: {check_msg}')

        # 获取用户信息
        info = session.get(USERINFO_URL, headers=HEADERS).json()
        total = info.get("transfer_enable", 0) / 1024**3       # 总流量 GB
        used = (info.get("u", 0) + info.get("d", 0)) / 1024**3  # 已用 GB
        left = total - used
        expire = info.get("expire_in", "未知")

        results.append(
            f"账号{i}（{email}）\n"
            f"签到: {check_msg}\n"
            f"已用流量: {used:.2f} GB / {total:.2f} GB\n"
            f"剩余流量: {left:.2f} GB\n"
            f"到期时间: {expire}\n"
        )
    except Exception as e:
        results.append(f"账号{i}（{email}）: 出错 - {e}")

# -------------------------------
# 循环完成后统一推送
# -------------------------------
final_content = '\n'.join(results)
push(final_content)
