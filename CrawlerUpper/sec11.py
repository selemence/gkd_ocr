import requests


url = 'https://www.python-spider.com/challenge/11'
session = requests.Session()
headers = {
        'Host': 'www.python-spider.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.python-spider.com',
        'Referer': 'https://www.python-spider.com/challenge/11',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
}
cookies = {
    'sessionid': 'ycgq6ll5jfie50vnou859v03om19yqkk'
}
session.headers.clear()
session.headers.update(headers)
response = session.get(url=url,headers=headers,cookies=cookies)
response2 = session.get(url=url,headers=headers,cookies=cookies)
print(response2.text)