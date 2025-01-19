import subprocess
import requests
import time

url = "https://www.python-spider.com/api/challenge21"

session = requests.Session()
headers = {
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
total_sum = 0

# 遍历从 1 到 100 的页码
for page in range(1, 101):
    result = subprocess.check_output(['node', r'sec21.js']).decode().split('\n')
    data ={"page" :page,
           "s":result[1],
           "t":result[0]}
    session.headers.clear()
    session.headers.update(headers)
    response = session.post(url,headers=headers,cookies=cookies,data=data) #此处verify=False以及加上代理本地请求可以requests库的阻止抓包检测 
    print(response.text)
    response_data = response.json()  
    data_list = response_data['data']
    for item in data_list:
        total_sum += int(item['value'])
                       
print(f"The total sum of all values is: {total_sum}")
