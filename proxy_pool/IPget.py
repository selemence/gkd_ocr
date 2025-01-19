import requests
import pandas as pd
import json
import time

def fetch_stock_data(page, size=90):
    url = f'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page={page}&size={size}&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
         'Cookie': 's=al120nzz0j; cookiesu=561720841063641; device_id=d17c0ab2542d1fd83c69d816b6f587d9; xq_a_token=64274d77bec17c39d7ef1934b7a3588572463436; xq_r_token=3f3592acdffbaaee3a7ea110c5d151d2710b7318; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcyMjczMjcyOCwiY3RtIjoxNzIwODU0OTU1ODA5LCJjaWQiOiJkOWQwbjRBWnVwIn0.io08PmP4oIYMJBrsuPImlIBQ01-wTePiwehVwNWBo6EU7ph8OyVYCe9JHawwEvPhuSWQv2FUX-2axP1PFAJqtxsOEW3-3tdqoCSxvNQ4wbFruNMaP2UeLYC3PW0_2xa0vV7gVyoX7afOhh6BdovJJToDA1MYdMRmNNiApxZFFje-ZLL2p9GVaWRfgDPe-yHkds3ffQlsM7enZagDgtVC3fvp9pf6CqcK2zhoSO51eWQoG6q8a3ST6NPk4zKwuzIBEDjNii8ciZYxFX3RrrWFMrTZ0RIpMOgiojk1RBSA3g3oL4RV8nHmk0F3y7clTji3Xc1e0pLMxXZ2orJoCb9ZdQ; u=561720841063641'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            print('Error decoding JSON')
            return None
    else:
        print(f'Failed to retrieve data: {response.status_code}')
        return None

def save_to_csv(data, filename='xueqiu_stock_data.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')

def main():
    all_data = []
    for i in range(1, 129):  # 爬取前128页的数据
        print(f'Fetching data for page {i}...')
        data = fetch_stock_data(page=i)
        if data:
            if 'data' in data and 'list' in data['data']:
                all_data.extend(data['data']['list'])
                # 每次爬取完一页数据后保存一次
                save_to_csv(all_data)
                print(f'Data from page {i} saved.')
            else:
                print('Unexpected data format:', data)
        time.sleep(1)  # 避免频繁请求被封禁

    print('All stock data saved to xueqiu_stock_data.csv')

if __name__ == '__main__':
    main()
