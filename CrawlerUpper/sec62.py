from curl_cffi import requests

def simulate_request():
    url = 'https://www.python-spider.com/api/challenge62'
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Host': '127.0.0.1',  # Update to correct host if needed
        'Pragma': 'no-cache',
        'Upgrade': 'websocket',
        'Connection': 'Upgrade',
        'Sec-WebSocket-Version': '13',
        'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }

    # 发起 GET 请求
    total_sum = 0
    for page in range(1,101):
        data = {'page' : page}
        response = requests.post(url=url, impersonate="Chrome101",data=data)
        print(response,response.text)
        # page_data = response['data']
        # num_list = sum([int(i['value']) for i in page_data])
        # total_sum += num_list
    print(total_sum)

if __name__ == '__main__':
    simulate_request()