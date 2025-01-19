import requests
import execjs

url = 'https://www.python-spider.com/api/challenge68'
headers = {
        'content-length': f'{len(payload)}',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.python-spider.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.python-spider.com/challenge/68',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
cookie = "3poojk0tc8zd27id7o4xj5es00z54d5k"

total = 0

def get_a(data):
    pass

for page in range(1,5):
    requ = requests.post(url)
    print(requ.text)
    data = {
        "uuid" : requ.uuid,
        "c" : requ.c,
        "r" : requ.r,
        "t" : requ.t,
        "a" : get_a(requ.text),
        "page" : page
    }
