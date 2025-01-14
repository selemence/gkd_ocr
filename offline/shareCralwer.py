import requests
import logging
import pandas as pd
import os
import time
import random
from hdfs import InsecureClient

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Cookie': 'cookiesu=401734153044017; xq_a_token=511bf5034992327eaaacb9d6ff05888641f2c88a; xqat=511bf5034992327eaaacb9d6ff05888641f2c88a; xq_r_token=6211e19e8993fdc1ed842755ff2f2940abc30988; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTczODI4NDkxNSwiY3RtIjoxNzM2MjQ5NDE0MTk4LCJjaWQiOiJkOWQwbjRBWnVwIn0.Sl__gCA8ypzUrjmmKZN9-OdHgs4JyWlzCwQKWUTVLeo-7YTYr1a9MhzthBaBzCe19dM4Pz1T2VvPvu3o1EKtOEs_wUXggG2ZuqDcZ1S5R2uzq6xfIG5jrgcTSZ3R0HGu57Un_Fn4sc7TMb9-22gYdTcYYP6LUFoU9m0dr6uT_AbJh97gNqzcpd0EwKHsdoiSrEUFGPbj8xCbcsLhAhH8rWP5gztGVqREqEuW3zRQ2QA5RYFK_AkHTqv3HLMUX2SEo3-6k-_GK4iYHWWsn8sJcs2m2c6k2ppAb2q7eFXw7dTHZDkxMLMPNXL2eqIEkSSD__4YIK-jqpPMwhrHVnQdtg; u=401734153044017; ssxmod_itna=QqUx0CF1GHGQDHQi5qeqODj2xAxmqi=hFtqsHHDlOPRDA5D8D6DQeGTQu1DB7l70rYqwW=C0pNtQ0RGNa/jAbW5aQVax0aDbqGkqf7rqqDx1q0rD74irDDxD3mxneD+D0bMgnkqi3DhxDODWKDXcckDipCDmbkvxGC/xDC2jPDwx0C0ODDBO0vKY9DlnY1kZAGF4D1qivPFnKD9hoDsP46KnImczLxBrHLXUA3vrYhDCKDjo7kDmWHF4xCS6Bqagxq72qqh0RDF0u51AGK10ZYFnhq8iGghjUi+PW3V7r9DDcNcdD==='
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

# 将数据保存到本地文件
def save_data_to_csv(data, filename):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')  # 指定编码为UTF-8
        logging.info(f'Data saved to file: {filename}')
    except IOError as e:
        logging.error(f'Error saving data to file: {e}')

def upload_to_hdfs(local_path, hdfs_path, hdfs_client):
    try:
        # 检查文件是否存在
        if hdfs_client.status(hdfs_path, strict=False):
            logging.info(f'File {hdfs_path} already exists. Deleting it.')
            hdfs_client.delete(hdfs_path)
        
        hdfs_client.upload(hdfs_path, local_path)
        logging.info(f'File {local_path} uploaded to HDFS at {hdfs_path}')
    except Exception as e:
        logging.error(f'Failed to upload file to HDFS: {e}')

# 处理单个URL的所有页面
def process_url(base_url):
    page = 1
    max_pages = 100  # 设置一个最大页数限制，避免无限请求
    all_data = []
    while page <= max_pages:
        url = f"{base_url}&page={page}"
        logging.info(f'Fetching data from URL: {url}')
        result = fetch_stock_data(url)
        if result and 'data' in result and 'list' in result['data']:
            page_data = result['data']['list']
            if not page_data:
                break  # 没有更多数据，停止翻页
            all_data.extend(page_data)
            
            # 添加随机延迟以避免反爬虫
            delay = random.uniform(1, 2)
            logging.info(f'Waiting for {delay:.2f} seconds to avoid detection')
            time.sleep(delay)
            
            page += 1
        else:
            logging.warning(f"No data found for URL: {url}")
            break  # 请求失败或没有数据，停止翻页
    return all_data

# 主程序
def main():
    base_url = 'https://stock.xueqiu.com/v5/stock/screener/quote/list.json'
    urls = [
        f'{base_url}?size=90&order=desc&order_by=percent&exchange=CN&market=CN&ind_code=S7103',
        f'{base_url}?size=30&order=desc&order_by=percent&market=HK&ind_code=7020&is_delay=true',
        f'{base_url}?size=30&order=desc&order_by=percent&market=US&ind_code=451030'
    ]
    all_data = []
    for base_url in urls:
        data = process_url(base_url)
        if data:  # 确保有数据
            df = pd.DataFrame(data)  # 将字典数据转换为DataFrame
            all_data.append(df)

    if all_data:
        logging.info("Combining all data into a single DataFrame")
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_filename = 'data/shareOfIndustry.csv'
        if not os.path.exists('data'):
            os.makedirs('data')
        combined_df.to_csv(combined_filename, index=False, encoding='utf-8')  # 指定编码为UTF-8
        logging.info(f'All data combined and saved to {combined_filename}')
        
        hdfs_url = 'http://192.168.160.141:9870'  # 替换为你的HDFS地址
        hdfs_client = InsecureClient(hdfs_url, user='root')  # 替换为你的HDFS用户名
        hdfs_path = '/flume/events/shareOfIndustry.csv'
        upload_to_hdfs(combined_filename, hdfs_path, hdfs_client)
    else:
        logging.warning("No data fetched to be saved or uploaded.")

    logging.info('Data fetched and uploaded to HDFS.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")