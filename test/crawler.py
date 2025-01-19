import requests
import pandas as pd
import logging
import time
from datetime import datetime
import os

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Cookie': 's=al120nzz0j; cookiesu=561720841063641; device_id=d17c0ab2542d1fd83c69d816b6f587d9; xq_a_token=aeb5755652c41b7828c9412ee90b26e08840b0c8; xqat=aeb5755652c41b7828c9412ee90b26e08840b0c8; xq_r_token=9ee9347bb54fea0445403de921297a01af9f4646; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcyNDAyODc2OCwiY3RtIjoxNzIxNTUzMjU5NTE4LCJjaWQiOiJkOWQwbjRBWnVwIn0.mVnXKS5WAOkDtQkc0z1e_JoGpP3RS1wBjBQRoNyTQW1sMNUPjXzfUPXidXhqU00477fU2V1OfqUDItUM74TuRhz7WzBTN3Mxi2fSNNIIFIYZZVu3V1GNmC9zJQKnkE62-_Tgvon4Yar9BzILiI3-uV7YjkswDORD5vk2fZ1Cyc1dWTCK6sp4WyU2uUoGoX7fDIcOVkTEHA7QqIGFQ-2JqjIHclu3I51kCpXFJHjK6uHT_h50McDwHh8e2JZ7Ve_-0OE7fZ6ohJEYamTbOjuhY8YCF4CciZktZj282_4H6CISK69jKJR4MSL22I395f-2_OsQ2GgRZ2mqVMw8yKHGtQ; u=561720841063641; is_overseas=0'
}

def date_to_timestamp(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    timestamp = int(dt.timestamp() * 1000)
    return timestamp

def get_stock_monthly_k_data(stock_code, start_date_str, end_date_str):
    start_timestamp = date_to_timestamp(start_date_str)
    end_timestamp = date_to_timestamp(end_date_str)
    
    url = f"https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={stock_code}&begin={start_timestamp}&end={end_timestamp}&period=day&type=before&count=-142"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'item' in data['data']:
            items = data['data']['item']
            columns = data['data']['column']
            
            df = pd.DataFrame(items, columns=columns)
            df['symbol'] = stock_code  # 添加symbol列
            return df
        else:
            logging.info(f"No data found for stock code {stock_code}.")
            return None
    else:
        logging.error(f"Failed to fetch data for stock code {stock_code}. Status code: {response.status_code}")
        return None

def fetch_stock_data(url):
    try:
        response = requests.get(url, headers=headers)
        logging.info(f'Request URL: {url}')
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f'Failed to retrieve data: {response.status_code} for URL: {url}')
            logging.error(f'Response Text: {response.text}')
            return None
    except requests.RequestException as e:
        logging.error(f'Request failed: {e} for URL: {url}')
        return None

def save_data_to_csv(data, filename):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        logging.info(f'Data saved to file: {filename}')
    except IOError as e:
        logging.error(f'Error saving data to file: {e}')

def main():
    # 获取多只股票的历史数据
    base_url = 'https://stock.xueqiu.com/v5/stock/screener/quote/list.json'
    urls = [f'{base_url}?&size=90&order=desc&order_by=percent&exchange=CN&market=CN&ind_code=S7103' for i in range(1, 3)]

    all_symbols = []

    for url in urls:
        result = fetch_stock_data(url)
        if result and 'data' in result and 'list' in result['data']:
            page_data = result['data']['list']
            symbols = [stock['symbol'] for stock in page_data]
            all_symbols.extend(symbols)
        else:
            logging.warning(f'No data retrieved from URL: {url}')
    
    logging.info(f'Total symbols fetched: {len(all_symbols)}')

    start_date_str = "2023-01-01"  # 替换为你需要的开始日期
    end_date_str = "2024-01-01"    # 替换为你需要的结束日期

    all_data = []

    for symbol in all_symbols:
        df = get_stock_monthly_k_data(symbol, start_date_str, end_date_str)
        if df is not None:
            all_data.append(df)
        time.sleep(1)  # 延迟1秒以减慢请求速度，避免被拒绝连接

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_filename = 'data/combined_monthly_k_data.csv'
        if not os.path.exists('data'):
            os.makedirs('data')
        combined_df.to_csv(combined_filename, index=False)
        logging.info(f'All data combined and saved to {combined_filename}')
    else:
        logging.warning('No data to combine.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
