import requests
import pandas as pd
import logging
import os

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Cookie': 's=al120nzz0j; cookiesu=561720841063641; device_id=d17c0ab2542d1fd83c69d816b6f587d9; xq_a_token=64274d77bec17c39d7ef1934b7a3588572463436; xq_r_token=3f3592acdffbaaee3a7ea110c5d151d2710b7318; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcyMjczMjcyOCwiY3RtIjoxNzIwODU0OTU1ODA5LCJjaWQiOiJkOWQwbjRBWnVwIn0.io08PmP4oIYMJBrsuPImlIBQ01-wTePiwehVwNWBo6EU7ph8OyVYCe9JHawwEvPhuSWQv2FUX-2axP1PFAJqtxsOEW3-3tdqoCSxvNQ4wbFruNMaP2UeLYC3PW0_2xa0vV7gVyoX7afOhh6BdovJJToDA1MYdMRmNNiApxZFFje-ZLL2p9GVaWRfgDPe-yHkds3ffQlsM7enZagDgtVC3fvp9pf6CqcK2zhoSO51eWQoG6q8a3ST6NPk4zKwuzIBEDjNii8ciZYxFX3RrrWFMrTZ0RIpMOgiojk1RBSA3g3oL4RV8nHmk0F3y7clTji3Xc1e0pLMxXZ2orJoCb9ZdQ; u=561720841063641'
}

# Flume 接收数据的 URL
FLUME_URL = 'http://192.168.160.141:44444'

# 请求数据
def fetch_stock_data(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f'Failed to retrieve data: {response.status_code}')
            return None
    except requests.RequestException as e:
        logging.error(f'Request failed: {e}')
        return None

# 保存数据到CSV并提交到Flume
def save_to_csv_and_flume(data, filename='xueqiu_stock_data.csv'):
    df = pd.DataFrame(data)
    df = df[['symbol','current', 'amount','name','pcf']]  # 筛选需要的列
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        df.to_csv(filename, index=False, encoding='utf-8-sig')

    # 提交数据到Flume
    try:
        payload_list = df.to_dict(orient='records')
        headers_flume = {'Content-Type': 'application/json'}
        response = requests.post(FLUME_URL, json=payload_list, headers=headers_flume)
        if response.status_code != 200:
            logging.error(f'Failed to send data to Flume: {response.status_code}')
        else:
            logging.info('Data sent to Flume successfully')
    except requests.RequestException as e:
        logging.error(f'Error sending data to Flume: {e}')

# 主程序
def main():
    all_data = []
    filename = 'xueqiu_data.csv'
    urls = [
        f'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page={i}&size=90&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz'
        for i in range(1, 58)
    ]

    for url in urls:
        result = fetch_stock_data(url)
        if result and 'data' in result and 'list' in result['data']:
            page_data = result['data']['list']
            save_to_csv_and_flume(page_data, filename)
            all_data.extend(page_data)
            logging.info(f'Saved data for URL: {url}')

    logging.info('Final data saved.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
