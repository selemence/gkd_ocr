import requests
import pandas as pd
import logging
import os
import time
import json

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Cookie': 's=al120nzz0j; cookiesu=561720841063641; device_id=d17c0ab2542d1fd83c69d816b6f587d9; xq_a_token=64274d77bec17c39d7ef1934b7a3588572463436; xq_r_token=3f3592acdffbaaee3a7ea110c5d151d2710b7318; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcyMjczMjcyOCwiY3RtIjoxNzIxMTAwNTAwMjU2LCJjaWQiOiJkOWQwbjRBWnVwIn0.X3jHVuy4ihqSRrFPRIcM7B1KDWy2dTHv4AOntLGOSqPXqvkKxwOCfMew7En5RkGjxXm2Lt8aoTSSVReW0iuH9xlTzDtWDQyg-coqeh0yknyHHSEQ1bKiD15-lEuWf6dU7PDhLPvxExOJPu7XGaQUC-74xo5S3pL251fWbP_kGH9zkJ3gO_FNGmevEuR95hUQYCaRh7DH-S_8RRk0UIuGX3k9sq8XKz3_b4MbWqDa7Dgxpent4JD4hXCQ6rmx5WufVwVZA6TMGnbskLlUAxoc1AfAQEjGirjA9-gUThn5EwnliAD-obvSOPK4jziql6aSq4_1zEj0rpLkiYDf699Vdg; u=561720841063641'}

# Flume 接收数据的 URL
FLUME_URL = 'http://192.168.160.141:44444'

# 请求数据
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

# 保存数据到CSV并提交到Flume
def save_to_csv_and_flume(data, filename='xueqiu_stock_data.csv'):
    df = pd.DataFrame(data)
    df = df[['symbol', 'current', 'amount', 'name']]  # 筛选需要的列
    
    # 删除含有 NaN 值的行
    df.dropna(inplace=True)
    
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        df.to_csv(filename, index=False, encoding='utf-8-sig')

    # 批量提交数据到Flume
    send_to_flume_in_batches(df)

# 向 Flume 发送数据的函数，带有重试逻辑
def send_to_flume_in_batches(df, batch_size=25, retries=3, delay=5):
    headers_flume = {'Content-Type': 'application/json'}
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i+batch_size]
        json_data = batch_df.to_json(orient='records')
        try:
            # 确保 JSON 数据格式正确
            parsed = json.loads(json_data)
        except json.JSONDecodeError as e:
            logging.error(f'JSON Decode Error: {e}')
            continue
        
        for attempt in range(retries):
            try:
                response = requests.post(FLUME_URL, json=parsed, headers=headers_flume)
                if response.status_code == 200:
                    logging.info(f'Batch {i // batch_size + 1} sent to Flume successfully')
                    break
                else:
                    logging.error(f'Failed to send batch {i // batch_size + 1} to Flume: {response.status_code}')
            except Exception as e:
                logging.error(f'Error sending batch {i // batch_size + 1} to Flume: {e}')
            
            time.sleep(delay)
        else:
            logging.error(f'Failed to send batch {i // batch_size + 1} to Flume after multiple attempts')
            return False
    return True

# 主程序
def main():
    all_data = []
    filename = 'xueqiu_data.csv'
    urls = [
        f'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page={i}&size=90&order=desc&orderby=percent&order_by=percent&market=HK&type=hk&is_delay=true'
        for i in range(1, 30)
    ] + [
        f'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page={i}&size=90&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz'
        for i in range(1, 58)
    ] + [
        f'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page={i}&size=90&order=desc&orderby=percent&order_by=percent&market=US&type=us'
        for i in range(1, 57)
    ]
    
    for url in urls:
        result = fetch_stock_data(url)
        if result and 'data' in result and 'list' in result['data']:
            page_data = result['data']['list']
            save_to_csv_and_flume(page_data, filename)
            all_data.extend(page_data)

    logging.info('Final data saved.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
