# var I = {
#         'page': String(k),
#         'token': md5(k['toString']())
#     };

import requests
import subprocess
import httpx

url ="https://www.python-spider.com/api/challenge58"
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
client = httpx.Client(http2=True)

def get_token(page):
    param = str(page)
    token = subprocess.check_output(['node', r'sec58.js',param]).decode().split('\n')
    print(token[0])
    return token[0]

def run():
    total_sum = 0
    for page in range(1,101):
        token = get_token(page)
        datas = {
            "page":page,
            "token":token
        }
        response = client.post(url=url,headers=headers,cookies=cookies,data=datas)
        print(response.text)
        response_data = response.json()
        data_list = response_data['data']
        num_list = sum([int(i['value']) for i in data_list])
        total_sum += num_list   
    print(total_sum)

    
if __name__ == '__main__':
    run()
