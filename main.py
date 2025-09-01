import requests
import os

# -------------------------------
# 配置推送
# -------------------------------
SCKEY = os.environ.get('SCKEY')
Token = os.environ.get('TOKEN')

# -------------------------------
# 多账号设置 (用 | 分隔)
# -------------------------------
emails = os.environ.get('EMAIL', '').split('|')
passwds = os.environ.get('PASSWD', '').split('|')

# -------------------------------
# 推送函数
# -------------------------------
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

# -------------------------------
# ikuuu 域名和接口
# -------------------------------
BASE_URL = 'https://ikuuu.de'
LOGIN_URL = f'{BASE_URL}/auth/login'
CHECKIN_URL = f'{BASE_URL}/user/checkin'
USERINFO_URLS = [
    f'{BASE_URL}/getuserinfo',   # 有的机场用这个
    f'{BASE_URL}/user/profile',  # 有的机场用这个
]

HEADERS = {
    'origin': BASE_URL,
    'referer': f'{BASE_URL}/auth/login',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': 'application/json, text/javascript, */*; q=0.01',
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
        resp = session.post(LOGIN_URL, headers=HEADERS, data=login_data, timeout=10).json()
        login_msg = resp.get('msg', '登录失败')
        print(f'账号{i}登录: {login_msg}')

        # 签到
        resp = session.post(CHECKIN_URL, headers=HEADERS, timeout=10).json()
        check_msg = resp.get('msg', '签到失败')
        print(f'账号{i}签到: {check_msg}')

        # 获取用户信息（尝试多个接口）
        info = None
        for url in USERINFO_URLS:
            try:
                tmp = session.get(url, headers=HEADERS, timeout=10).json()
                if "transfer_enable" in tmp or "u" in tmp:
                    info = tmp
                    break
            except Exception:
                continue

        if info:
            total = info.get("transfer_enable", 0) / 1024**3
            used = (info.get("u", 0) + info.get("d", 0)) / 1024**3
            left = total - used
            expire = info.get("expire_in", "未知")

            results.append(
                f"账号{i}（{email}）\n"
                f"签到: {check_msg}\n"
                f"已用流量: {used:.2f} GB / {total:.2f} GB\n"
                f"剩余流量: {left:.2f} GB\n"
                f"到期时间: {expire}\n"
                "-------------------------"
            )
        else:
            results.append(
                f"账号{i}（{email}）\n"
                f"签到: {check_msg}\n"
                f"⚠️ 未能获取流量/到期时间\n"
                "-------------------------"
            )

    except Exception as e:
        results.append(f"账号{i}（{email}）: 出错 - {e}\n-------------------------")

# -------------------------------
# 循环完成后统一推送
# -------------------------------
final_content = "\n".join(results)
print("推送内容:\n", final_content)  # 调试
push(final_content)
