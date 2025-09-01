👌 明白了，现在确认：

* `/user/profile` 返回的并不是 JSON（要么是跳转登录页，要么前端用 JS 渲染）。
* `/user` 页面返回的是个空壳 HTML，没有直接写明流量和到期时间。
* 所以我们需要 **找 ikuuu 的真实数据接口**，而不是硬解析 HTML。

---

### ✅ 通常机场的接口规律

很多魔改 ssrpanel / v2board 的站点，都会有一个 JSON 接口：

* `https://ikuuu.de/getuserinfo`
* 或 `https://ikuuu.de/api/v1/user/getSubscribe`
* 或 `https://ikuuu.de/user/info`

这些接口里通常包含：

```json
{
  "data": {
    "u": 12345678,
    "d": 87654321,
    "transfer_enable": 107374182400,
    "expired_at": "2025-09-30 23:59:59"
  }
}
```

---

### 🔧 建议下一步

我帮你写一个测试脚本，直接尝试请求 **几个常见 API**，把结果原样打印出来，这样就能锁定正确的接口。

```python
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
    resp = session.post(LOGIN_URL, headers=HEADERS, data=login_data, timeout=10).json()
    print(f"账号{i}登录: {resp.get('msg')}")

    for api in TEST_APIS:
        url = BASE_URL + api
        try:
            r = session.get(url, headers=HEADERS, timeout=10)
            print(f"尝试 {api} 状态: {r.status_code}")
            print("返回内容预览:", r.text[:200], "\n---")
        except Exception as e:
            print(f"访问 {api} 出错: {e}")
```

---

### 📌 你需要做的

1. 在 GitHub Actions 里跑这段测试代码。
2. 看日志里哪个接口返回了 JSON，并且里面有 `u / d / transfer_enable / expired_at` 之类的数据。
3. 把返回的 JSON 样例贴给我，我帮你写提取逻辑（剩余流量、到期时间）。

---

要不要我帮你改成一个 **debug 分支的 workflow**，单独跑这个接口探测，不影响你现在的签到脚本？
