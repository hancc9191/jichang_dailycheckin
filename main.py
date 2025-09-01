import requests
import os

emails = os.environ.get('EMAIL', '').split('|')
passwds = os.environ.get('PASSWD', '').split('|')

BASE_URL = 'https://ikuuu.de'
LOGIN_URL = f'{BASE_URL}/auth/login'
HEADERS = {
    'origin': BASE_URL,
    'referer': f'{BASE_URL}/auth/login',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}

TEST_APIS = [
    "/getuserinfo",
    "/user/getSubscribe",
    "/api/v1/user/info",
    "/api/v1/user/getSubscribe",
    "/user/profile",
]

for i, (email, passwd) in enumerate(zip(emails, passwds), start=1):
    session = requests.Session()
    login_data = {'email': email, 'passwd': passwd}
    try:
        resp = session.post(LOGIN_URL, headers=HEADERS, data=login_data, timeout=10).json()
        print(f"账号{i} 登录结果: {resp.get('msg')}")
    except Exception as e:
        print(f"账号{i} 登录请求失败: {e}")
        continue

    for api in TEST_APIS:
        url = BASE_URL + api
        try:
            r = session.get(url, headers=HEADERS, timeout=10)
            print(f"尝试 {api}, 状态码: {r.status_code}")
            print("返回内容预览:", r.text[:200].replace("\n", " "), "\n---")
        except Exception as e:
            print(f"访问 {api} 出错: {e}")
