import json
import httpx
import logging

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
    'sessionid': 'bh6qvnseejgodmn27j54u3puqa2d0iis'
}
max_count = 0
for i in range(51,52):
    client = httpx.Client(http2=True)
    try:
        data = {
            'page': str(i)
            }
        res = client.post(url="https://www.python-spider.com/api/challenge59", headers=headers, data=data,
        cookies=cookies).json()
        count = res['data']
        print(res)
        num_list = sum([int(i['value']) for i in count])
        max_count += num_list
    except Exception as e:
        logging.error(f"An error occurred: {e}")
print(max_count)
client.close()