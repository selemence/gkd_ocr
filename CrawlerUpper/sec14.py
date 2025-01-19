import subprocess
import requests

url = "https://www.python-spider.com/api/challenge14"

session = requests.Session()
headers = {
        'Host': 'www.python-spider.com',
        'Content-Length': '6',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.python-spider.com',
        'Referer': 'https://www.python-spider.com/challenge/14',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
}

cookies = {
    'sessionid': 'ycgq6ll5jfie50vnou859v03om19yqkk'
}
total_sum = 0

# 遍历从 1 到 100 的页码
for page in range(1, 101):
    param = str(page)
    result = subprocess.run(['node', r'sec14.js',param], shell=True, capture_output=True, text=True)
    data ={"page" :page,
           "uc":result.stdout}
    session.headers.clear()
    session.headers.update(headers)
    response = session.post(url,headers=headers, cookies=cookies,data=data,proxies={}) #此处verify=False以及加上代理本地请求可以requests库的阻止抓包检测 
    response_data = response.json()  
    data_list = response_data['data']
    for item in data_list:
        total_sum += int(item['value'])
                       
print(f"The total sum of all values is: {total_sum}")
