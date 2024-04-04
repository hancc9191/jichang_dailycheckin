import requests
import json
import re
import os

session = requests.session()

# Function to send notification


# Login URLs
login_url = 'https://ikuuu.pw/auth/login'
check_url = 'https://ikuuu.pw/user/checkin'
info_url = 'https://ikuuu.pw/user/profile'

# User credentials list
users = [
    {'email': os.environ.get('EMAIL'), 'passwd': os.environ.get('PASSWD'), },
    {'email': os.environ.get('EMAIL1'), 'passwd': os.environ.get('PASSWD1'), }
]

# Headers
header = {
    'origin': 'https://ikuuu.me',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

# Loop through each user
for user in users:
    try:
        print(f"Logging in for {user['email']}...")
        # Perform login
        data = {'email': user['email'], 'passwd': user['passwd']}
        response = json.loads(session.post(url=login_url, headers=header, data=data).text)
        print(response['msg'])
        
        # Fetch user profile information
        info_html = session.get(url=info_url, headers=header).text

        # Perform check-in
        result = json.loads(session.post(url=check_url, headers=header).text)
        print(result['msg'])
        content = result['msg']

        # Send notification
        push(content)
    except Exception as e:
        content = f"签到失败: {str(e)}"
        print(content)
        push(content)
