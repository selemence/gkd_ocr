import requests
import time
import base64
import hashlib


def md5_value(key):
    input_name = hashlib.md5()
    input_name.update(key.encode("utf-8"))
    sign = (input_name.hexdigest()).lower()
    return sign


def base64_value(key):
    base64_a_timestamp = base64.b64encode(key.encode('utf8'))
    base64_str = str(base64_a_timestamp, 'utf-8')
    return base64_str

url = "https://www.python-spider.com/api/challenge1"

def set_safe(timestamp):
    a = '9622'
    encrypt_str = a + timestamp
    token = base64_value(encrypt_str)
    safe = md5_value(token)
    return safe

cookies = {
    "sessionid": 'ycgq6ll5jfie50vnou859v03om19yqkk',
    }

total_sum = 0

# 遍历从 1 到 100 的页码
for page in range(1, 101):
    timestamp = str(int(time.time()))
    safe = set_safe(timestamp)
    headers = {
        'safe': safe,
        'timestamp': timestamp,
    }
    data = {"page": page}
    response = requests.post(url,headers=headers,cookies=cookies,data=data) #此处verify=False以及加上代理本地请求可以requests库的阻止抓包检测
    response_data = response.json()  
    
    data_list = response_data['data']
    for item in data_list:
        total_sum += int(item['value'])
                       
print(f"The total sum of all values is: {total_sum}")