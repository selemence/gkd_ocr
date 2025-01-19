import requests

url = "https://www.python-spider.com/api/challenge7"


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'cookie' : "sessionid=ycgq6ll5jfie50vnou859v03om19yqkk; Hm_lvt_337e99a01a907a08d00bed4a1a52e35d=1728028273,1728047001,1728047966,1728111015; HMACCOUNT=49F210C37DAC9434; no-alert=true; Hm_lpvt_337e99a01a907a08d00bed4a1a52e35d=1728114402",
}
total_sum = 0

# 遍历从 1 到 100 的页码
for page in range(1, 101):
    data = {"page": page}
    requests.post('https://www.python-spider.com/cityjson')
    response = requests.post(url,headers=headers,data=data) #此处verify=False以及加上代理本地请求可以requests库的阻止抓包检测
    response.raise_for_status()  
    response_data = response.json()  
    data_list = response_data['data']
    for item in data_list:
        total_sum += int(item['value'])
                       
print(f"The total sum of all values is: {total_sum}")