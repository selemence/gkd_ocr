
import logging
import time
import requests
import threading

CONFIG_DIC = {
    # 定时循环检查的时间间隔,单位秒
    "check_interval": 60*60,
    # 连接超时时间,单位秒
    "timeout": 2,
    # 重试次数
    "retry": 4,
    # 检测代理可用性的URL, 例如 "http://baidu.com"
    "check_url": "https://phoile.goldmine168.com/en/sports"
}
# 请求头
headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'priority': 'u=1, i',
    'Referer': 'https://phoile.goldmine168.com/en/sports',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# ================== start code =========================
# 检查代理结果
test_proxies_dic = {"good_list": [], "bad_list": []}

def eval_to_dict(line):
    if line.strip().endswith(','):
        line = line.strip()[:-1]
    else:
        line = line.strip()
    return eval(line)

def load_proxies_from_file(filename='proxies.txt'):
    '''
    加载代理列表，从文件proxies.txt中读取
        {"address": "119.91.32.68", "port": 14693, "user": "123", "password": "123"}
    '''
    try:
        with open(filename, 'r') as f:
            proxies_list = [eval_to_dict(line) for line in f.readlines() if line.strip()]
        logging.info(f'Loaded {len(proxies_list)} proxies from proxies.txt')
    except FileNotFoundError:
        logging.error('File proxies.txt not found')
    except Exception as e:
        logging.error(f'Error loading proxies: {e}')
    return proxies_list


# 日志配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='yb_proxy_check.log',
                    filemode='a')

def check_proxie(proxy):
    try:
        # 重试次数
        retry = CONFIG_DIC["retry"]
        while retry > 0:
            try:
                proxies = {'http': f'http://{proxy["user"]}:{proxy["password"]}@{proxy["address"]}:{proxy["port"]}',
                           'https': f'http://{proxy["user"]}:{proxy["password"]}@{proxy["address"]}:{proxy["port"]}'}
                response = requests.get(CONFIG_DIC["check_url"],headers=headers, proxies=proxies, timeout=CONFIG_DIC["timeout"])
                # print(response.status_code, response.text)
                if response.status_code == requests.codes.ok:
                    test_proxies_dic["good_list"].append(proxy)
                    logging.info(f'Proxy {proxy["address"]} is working')
                    break
                else:
                    retry -= 1
            except requests.exceptions.RequestException as e:
                retry -= 1
            except Exception as e:
                retry -= 1
        if retry == 0:
            logging.error(f'Proxy {proxy["address"]} is not working')
            test_proxies_dic["bad_list"].append(proxy)
    except Exception as e:
        logging.error(f'Error checking proxy {proxy["address"]}: {e}')
        test_proxies_dic["bad_list"].append(proxy)
        

def main():
    proxies_list = load_proxies_from_file("yb_proxies.txt")
    logging.info('Proxy check started')
    while True:
        try:
            threads = []
            for proxy in proxies_list:
                t = threading.Thread(target=check_proxie, args=(proxy,))
                threads.append(t)
                t.start()
            
            for t in threads:
                t.join()
            
            with open('yb_proxies_good.txt', 'w') as fa, open('yb_proxies_bad.txt', 'w') as fb:
                for proxy in test_proxies_dic["good_list"]:
                    fa.write(str(proxy) + '\n')
                for proxy in test_proxies_dic["bad_list"]:
                    fb.write(str(proxy) + '\n')
                logging.info(f'Good proxies: {len(test_proxies_dic["good_list"])}')
                logging.info(f'Bad proxies: {len(test_proxies_dic["bad_list"])}')
                logging.info('Proxy check completed')
                print(f'Good proxies: {len(test_proxies_dic["good_list"])}, Bad proxies: {len(test_proxies_dic["bad_list"])}')
                test_proxies_dic["good_list"].clear()
                test_proxies_dic["bad_list"].clear()
            time.sleep(CONFIG_DIC["check_interval"])  
        except Exception as e:
            for t in threads:
                t.join()
            logging.error(f'Error in main loop: {e}')
            
if __name__ == '__main__':
    # 多进程检查代理
    import multiprocessing
    multiprocessing.Process(target=main).start()
    
    # proxy = {'address': '52.175.38.113', 'port': 27054, 'user': '123', 'password': '123'}
    # check_proxie(proxy)

    # print(load_proxies_from_file())
    
    
    

