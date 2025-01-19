import requests

url = "https://www.python-spider.com/api/challenge6"
cookie = {
    "sessionid": "ycgq6ll5jfie50vnou859v03om19yqkk",
}

session = requests.Session()
total_sum = 0

# 遍历从 1 到 100 的页码
for page in range(1, 101):
    data = {"page": page}
    response = session.post(url, cookies=cookie, data=data)
    response.raise_for_status()  
    response_data = response.json()  
    data_list = response_data['data']
    for item in data_list:
        total_sum += int(item['value'])
                       
session.close()
print(f"The total sum of all values is: {total_sum}")