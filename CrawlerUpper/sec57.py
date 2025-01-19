import subprocess
import requests
import json

url = "https://www.python-spider.com/api/challenge57"

session = requests.Session()
headers = {
        'Host': 'www.python-spider.com',
        'Content-Length': '6',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.python-spider.com',
        'Referer': 'https://www.python-spider.com/challenge/57',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
}

cookies = {
    'sessionid': 'ycgq6ll5jfie50vnou859v03om19yqkk'
}
total_sum = 0

for page in range(1, 101):
    data ={"page" :page,}
    session.headers.clear()
    session.headers.update(headers)
    response = session.post(url,headers=headers, cookies=cookies,data=data,proxies={}) #此处verify=False以及加上代理本地请求可以requests库的阻止抓包检测 
    param = response.text
    scrs =json.loads(param)
    scrs = scrs['result']
    result = subprocess.run(['node', r'sec57.js',scrs], shell=True, capture_output=True, text=True)
    suc = result.stdout
    response_data = json.loads(suc)
    data_list = response_data['data']
    for item in data_list:
        total_sum += int(item['value'])
                       
print(f"The total sum of all values is: {total_sum}")






