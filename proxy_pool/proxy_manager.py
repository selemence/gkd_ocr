import aiohttp
import pandas as pd
import asyncio
import aioredis
import json
import logging
import itertools

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = 'root' 
PROXY_KEY = 'use_proxy'

class ProxyManager:
    def __init__(self, redis_host=REDIS_HOST, redis_port=REDIS_PORT, redis_password=REDIS_PASSWORD, proxy_key=PROXY_KEY):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password
        self.proxy_key = proxy_key
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(
            f"redis://{self.redis_host}:{self.redis_port}",
            password=self.redis_password,
            decode_responses=True
        )
        logging.info("Connected to Redis")

    async def get_proxies(self):
        try:
            proxies = await self.redis.hgetall(self.proxy_key)
            proxy_list = []
            for proxy, details in proxies.items():
                try:
                    details_json = json.loads(details)
                    ip_port = details_json.get("proxy")
                    if ip_port:
                        proxy_list.append(ip_port)
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON for proxy {proxy}: {e}")
            logging.info(f"Retrieved {len(proxy_list)} proxies from Redis")
            return proxy_list
        except aioredis.exceptions.ResponseError as e:
            logging.error(f"Error fetching proxies from Redis: {e}")
            return []

    async def close(self):
        await self.redis.close()
        logging.info("Closed Redis connection")

# 异步请求数据
async def fetch_stock_data(session, page, size=90, proxy=None):
    url = f'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page={page}&size={size}&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Cookie': 's=al120nzz0j; cookiesu=561720841063641; device_id=d17c0ab2542d1fd83c69d816b6f587d9; xq_a_token=64274d77bec17c39d7ef1934b7a3588572463436; xq_r_token=3f3592acdffbaaee3a7ea110c5d151d2710b7318; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcyMjczMjcyOCwiY3RtIjoxNzIwODU0OTU1ODA5LCJjaWQiOiJkOWQwbjRBWnVwIn0.io08PmP4oIYMJBrsuPImlIBQ01-wTePiwehVwNWBo6EU7ph8OyVYCe9JHawwEvPhuSWQv2FUX-2axP1PFAJqtxsOEW3-3tdqoCSxvNQ4wbFruNMaP2UeLYC3PW0_2xa0vV7gVyoX7afOhh6BdovJJToDA1MYdMRmNNiApxZFFje-ZLL2p9GVaWRfgDPe-yHkds3ffQlsM7enZagDgtVC3fvp9pf6CqcK2zhoSO51eWQoG6q8a3ST6NPk4zKwuzIBEDjNii8ciZYxFX3RrrWFMrTZ0RIpMOgiojk1RBSA3g3oL4RV8nHmk0F3y7clTji3Xc1e0pLMxXZ2orJoCb9ZdQ; u=561720841063641'
    }
    try:
        async with session.get(url, headers=headers, proxy=f"http://{proxy}" if proxy else None) as response:
            if response.status == 200:
                try:
                    return await response.json()
                except aiohttp.ContentTypeError:
                    logging.error(f'Error decoding JSON from page {page}')
                    return None
            else:
                logging.error(f'Failed to retrieve data from page {page}: {response.status}')
                return None
    except aiohttp.ClientConnectorError as e:
        logging.error(f'Proxy connection error for proxy {proxy}: {e}')
        return None

# 保存数据到CSV
def save_to_csv(data, filename='xueqiu_stock_data.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')

# 主程序
async def main():
    all_data = []
    proxy_manager = ProxyManager()
    await proxy_manager.connect()
    proxies = await proxy_manager.get_proxies()
    await proxy_manager.close()
    proxy_cycle = itertools.cycle(proxies)  # 创建一个循环迭代器来轮询代理

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 129):  # 爬取前128页的数据
            proxy = next(proxy_cycle, None)  # 获取下一个代理
            tasks.append(fetch_stock_data(session, i, proxy=proxy))
            if len(tasks) >= 10:  # 每10个任务一批
                results = await asyncio.gather(*tasks)
                for result in results:
                    if result and 'data' in result and 'list' in result['data']:
                        all_data.extend(result['data']['list'])
                save_to_csv(all_data)
                logging.info(f'Data up to page {i} saved.')
                tasks = []
                await asyncio.sleep(1)  # 避免频繁请求被封禁

        # 处理剩余的任务
        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                if result and 'data' in result and 'list' in result['data']:
                    all_data.extend(result['data']['list'])
            save_to_csv(all_data)
            logging.info('Final data saved.')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An error occurred: {e}")
