import requests
import subprocess
import requests
import execjs
import logging


def get_results(page):
    headers = {
        'authority': 'www.python-spider.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'page': page,
    }
    des_data = subprocess.run(['node', r'sec60.js',str(page)], shell=True, capture_output=True, text=True).stdout
    url = f'https://www.python-spider.com/api/challenge60/{des_data}'
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# def decode(encrypted_str):
#     KEY = 'aiding6666666666'
#     key = KEY.encode('utf-8')
#     encrypted_data = base64.b64decode(encrypted_str)
#     cipher = DES.new(key, DES.MODE_ECB)
#     decrypted_data = unpad(cipher.decrypt(encrypted_data), DES.block_size)
#     return decrypted_data.decode('utf-8')

def parse():
    count = 0
    for page in range(1, 101):
        results = get_results(str(page))
        data_list = results['data']
        for data in data_list:
            count += int(str(data['value']).strip())
        print(f'前 {page} 页之和为: {count}')
    print(f'本题答案为: {count}')  # 本题答案为: 5004204 4997534


if __name__ == '__main__':
    parse()