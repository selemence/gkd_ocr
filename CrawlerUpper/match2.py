import subprocess
import time
import requests

session = requests.Session()
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-length': '0',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://match2023.yuanrenxue.cn/topic/2',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}
cookie = {
    'sessionid': 'vsugs8lnbxdxmnx8otrskyeloc8u3fdq'
}

s = 0
for page in range(1,6):
    token = subprocess.check_output(['node', r'test_match2.js',str(page)]).decode().split('\n')[0]
    print(token)
    params = {
        'page' : page,
        'token' : token
    }
    session.headers.clear()
    session.headers.update(headers)
    response = session.post('https://match2023.yuanrenxue.cn/api/match2023/2', headers=headers,cookies=cookie,params=params)
    print(response, response.text)
    s += sum(x['value'] for x in response.json()['data'])
    
print(s)
 