import aiohttp
import asyncio
import random
from proxy_manager import get_proxy

# 异步请求函数
async def fetch(session, url, proxy):
    try:
        async with session.get(url, proxy=f"http://{proxy}") as response:
            return await response.text()
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# 异步爬虫
async def fetch_all(urls, proxies):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            proxy = random.choice(proxies)  # 从代理池中随机选择一个代理
            task = fetch(session, url, proxy)
            tasks.append(task)
        return await asyncio.gather(*tasks)

# 主函数
async def main(urls, concurrent_requests):
    proxies = await get_proxy()
    if not proxies:
        print("No proxies available")
        return
    
    for i in range(0, len(urls), concurrent_requests):
        batch = urls[i:i + concurrent_requests]
        results = await fetch_all(batch, proxies)
        for result in results:
            if result:
                print(result)  # 或者处理结果
        await asyncio.sleep(1)  # 控制每秒并发量

# 示例URL列表
urls = ["https://76.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112403537215500227666_1720841250877"
        "&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&dect=1&wbp2u=|0|0|0|web&fid=f3&fs=m:1+t:2,m:1+t:23"
        ,"https://xueqiu.com/stock#exchange=CN&firstName=1&secondName=1_0"] 

# 设置每秒并发量
concurrent_requests = 50

# 运行主函数
if __name__ == '__main__':
    asyncio.run(main(urls, concurrent_requests))
