import json
import httpx
import logging

data = {
'page': '2'
}
headers={
    'method': 'POST',
    'authority': '',
    'scheme': 'https',
    'path': '/api/challenge24',
    'sec-ch-ua':'"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'accept':'application/json, text/javascript, */*; q=0.01',
    'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
    'x-requested-with':'XMLHttpRequest',
    'sec-ch-ua-mobile':'?0',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'sec-ch-ua-platform':'"Windows"',
    'origin':'',
    'sec-fetch-site':'same-origin',
    'sec-fetch-mode':'cors',
    'sec-fetch-dest':'empty',
    'referer':'',
    'accept-encoding':'gzip, deflate, br',
}
cookies = {
    'sessionid': 'ycgq6ll5jfie50vnou859v03om19yqkk'
}
max_count = 0
for i in range(1,101):
    client = httpx.Client(http2=True)
    try:
        data = {
            'page': str(i)
            }
        res = client.post(url="https://www.python-spider.com/api/challenge24", headers=headers, data=data,
        cookies=cookies).json()
        count = res['data']
        num_list = sum([int(i['value']) for i in count])
        max_count += num_list
        print('----------')
        print(num_list)
        print(max_count)
        print('----------')
    except Exception as e:
        logging.error(f"An error occurred: {e}")

client.close()