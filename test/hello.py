import requests
import pandas as pd
import logging
import json
import socket

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Cookie': 's=al120nzz0j; cookiesu=561720841063641; device_id=d17c0ab2542d1fd83c69d816b6f587d9; smidV2=202407131607415c71367525dea453b8260d92ac3473c7009805141ed7901f0; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=ebDXZpYf4iYy/Q//fNnpVPWIxXqwAw3Y8LTzhDaaJ4xs2yB/ijASAuaDe6ULuTdyHFTr1KSaNkJB5kThd7tJ7Q%3D%3D; acw_tc=276077a417211860336126468e0d72440aebdcae4cb7b9e480eb54748cfd97; xq_a_token=64274d77bec17c39d7ef1934b7a3588572463436; xq_r_token=3f3592acdffbaaee3a7ea110c5d151d2710b7318; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcyMjczMjcyOCwiY3RtIjoxNzIxMTg2MDIzMTAyLCJjaWQiOiJkOWQwbjRBWnVwIn0.DjD5NoNEbCmxE3OGXw1ZNO5m8FSpiJPQQ98Fe3nJBeTJ7me5YiXohimRhi0prZu-ZHkLteFhVwGGw1J2MB-KOleb8ie4WrNDSdIvZ9jYbgkqeuCiCUOsiT99p2RRy9kpbeyYRGaWcmeaVHOFGXFWLwZwLjE_26vZ-2qAZ_-_YUl6tg6Zknrsq-IXw_1AulWGN5VCntGGkTJqBRwXGZzCRB3eiVmKswjjdlQaQ3tBJTKUOzbFepJflDqAj1EBRfi2ZIKTgEA8lehgByeFtYFtkERaMvuk62qpQuQvx3iRQXI1NPXgH9rM19g0TU8X-BesVtKW7anBlvm0G7hVNhae1A; u=561720841063641'
}

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

# 向 Flume 发送数据的函数，使用 socket
def send_to_flume(data, host, port):
    try:
        logging.info('Attempting to send data to Flume')
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        # 发送数据
        client_socket.sendall((data + "\n").encode('utf-8'))
        logging.info(f'Data sent to Flume successfully: {data}')
        
        client_socket.close()
    except Exception as e:
        logging.error(f'Error sending data to Flume: {e}')

# 验证数据格式的函数
def is_valid_record(record):
    try:
        required_keys = ['symbol', 'current', 'amount']
        for key in required_keys:
            if key not in record:
                logging.warning(f"Missing key {key} in record: {record}")
                return False
        return True
    except Exception as e:
        logging.warning(f"Error validating record: {record}, error: {e}")
        return False

# 主程序
def main():
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
        logging.info(f'Fetching data from URL: {url}')
        result = fetch_stock_data(url)
        if result and 'data' in result and 'list' in result['data']:
            page_data = result['data']['list']
            df = pd.DataFrame(page_data)
            df = df[['symbol', 'current', 'amount']]  # 筛选需要的列
            
            # 删除含有 NaN 值的行
            df.dropna(inplace=True)
            
            json_data = df.to_json(orient='records')
            logging.info(f'JSON data to be sent: {json_data}')
            
            # 验证每条记录，并过滤掉不符合格式的数据
            valid_records = [record for record in json.loads(json_data) if is_valid_record(record)]
            if valid_records:
                for record in valid_records:
                    filtered_json_data = json.dumps(record)
                    logging.info(f'Sending filtered data to Flume: {filtered_json_data}')
                    send_to_flume(filtered_json_data, '192.168.160.141', 44444)  # 替换为你的 Flume 地址和端口
            else:
                logging.warning("No valid records to send to Flume")

    logging.info('Data fetched and sent to Flume.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
