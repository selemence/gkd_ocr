import re
import time
import json
import redis
import random
import hashlib
import datetime
import itertools
import threading
from flask import Flask
from curl_cffi import requests
from logger import Logger
import traceback

from init_data import init_odds
from yb_random_ip import random_proxies

logger = Logger().get_logger()

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
score_info = {}
app = Flask(__name__)
mids_list = []
host = ['www.iwon8game.vip', 'www.iwon88fun.xyz']

user_info = [
    {'account': '2blvkka', 'password': 'xiaoqian123'},
    {'account': 'myslqkw', 'password': 'xiaoqian123'},
    {'account': 'wcngsn', 'password': 'xiaoqian123'},
    {'account': 'qe1hjls', 'password': 'xiaoqian123'},
    {'account': 'nhf2f7', 'password': 'xiaoqian123'}
]

def password_exec(password):
    md5 = hashlib.md5()
    md5.update(password.encode("utf-8"))
    digest = md5.hexdigest().upper()
    return digest[8:24]

def get_authorization(u_info):
    while True:
        try:
            api = random.choice(host)
            proxies = random_proxies()
            data = {
                'login_form[user-name]': u_info["account"],
                'login_form[password]': password_exec(u_info["password"]),
                'fingerPrint': '342158876',
                'method': 'login',
                'system_data[current_url]': 'https://www.iwon8game.com/Default.aspx'
            }
            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://www.iwon8game.com",
                "Pragma": "no-cache",
                "Referer": "https://www.iwon8game.com/games/PSport.aspx",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "sec-ch-ua-mobile": "?0"
            }
            response = requests.post(f'https://{api}/WebHandler/AuthService.ashx', 
                                     data=data, proxies=proxies,
                                     timeout=10,
                                     impersonate="chrome110", headers=headers)
            if response.status_code != 200:
                raise Exception(f"用户 {u_info['account']} 登录失败: {response.status_code}")
            if response.json()["status"] != "success":
                raise Exception(f"用户 {u_info['account']} 登录失败: {response.json()['message']}")

            cookies = {
                'ASP.NET_SessionId': response.cookies.get('ASP.NET_SessionId'),
                'Language': 'zh-cn',
                'login': response.cookies.get('login'),
                'MainCookie': 'active=cookie still active',
            }
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Referer': 'https://www.iwon8game.vip/Default.aspx',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            response = requests.get(f'https://{api}/games/PSport.aspx', 
                                    proxies=proxies, 
                                    timeout=10,
                                    impersonate="chrome110",
                                    headers=headers, cookies=cookies)
            if response.status_code != 200 or not re.findall('token=(.*?)"', response.text):
                raise Exception(f"用户 {u_info['account']} 获取token失败")
            token = re.findall('token=(.*?)"', response.text)[0]

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'priority': 'u=0, i',
                'referer': 'https://3.33.215.100/',
                'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'iframe',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'cross-site',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            }

            params = {
                'locale': 'zh-cn',
                'sport': 'soccer',
                'oddsFormat': 'EU',
                'mode': 'LIGHT',
                'target': 'LIVE',
                'token': token,
                'detectedUrl': 'https://phoile.checker99.com'
            }

            response = requests.get('https://phoile.checker99.com/member-service/v2/login-token', 
                                    params=params,
                                    allow_redirects=False, 
                                    proxies=proxies, 
                                    timeout=20, 
                                    impersonate="chrome110",
                                    headers=headers)
            if not response.status_code == 302 and not response.headers.get("Set-Cookie"):
                raise Exception(f"用户 {u_info['account']} 最终登录错误")

            u_info['cookies'] = {
                "JSESSIONID": response.cookies.get("JSESSIONID"),
                'BrowserSessionId_79': response.cookies.get("BrowserSessionId_79"),
                'SLID_79': response.cookies.get("SLID_79"),
                '__prefs': response.cookies.get("__prefs"),
                '_ulp': response.cookies.get("_ulp"),
                'custid_79': response.cookies.get("custid_79"),
                'lcu': response.cookies.get("lcu"),
                'pctag': response.cookies.get("pctag"),
                'u_79': response.cookies.get("u_79"),
                'uoc': response.cookies.get("uoc"),
                'HMF_CI': response.cookies.get("HMF_CI")
            }
            u_info['proxies'] = proxies
            logger.info(f"登录成功: {u_info['account']}")
            return True
        except requests.RequestsError:
            pass
        except Exception as e:
            logger.error(f"错误信息： {e}")
            # print(traceback.format_exc())

def login_check(u_info):
    try:
        cookies = u_info.get('cookies')
        if not cookies:
            logger.error(f"login_check:用户 {u_info['account']} cookies不存在")
            return False
        
        proxies = u_info.get("proxies")
        if not proxies:
            logger.error(f"login_check:用户 {u_info['account']} proxies不存在")
            proxies = random_proxies()
            u_info['proxies'] = proxies
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://phoile.goldmine168.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://phoile.goldmine168.com/zh-cn/compact/sports/soccer',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'locale': 'zh_CN',
            '_': str(int(time.time() * 1000)),
            'withCredentials': 'true',
        }

        response = requests.post(
            'https://phoile.goldmine168.com/member-service/v2/account-balance',
            params=params,
            cookies=cookies,
            headers=headers,
            proxies=proxies,
            impersonate="chrome110"
        )
        if response.status_code != 200 or not response.json().get('loginId'):
            return False
        return True
    except Exception as e:
        logger.error(f"login_check:error: {e}")
        print(traceback.format_exc())
        return True


def get_mids(u_info):
    try:
        global mids_list
        proxies = u_info.get('proxies')
        cookies = u_info.get('cookies')
        if not cookies:
            logger.error(f"getMatchOddsInfo2PB: cookies is None") 
            return False
        if not proxies:
            logger.error(f"getMatchOddsInfo2PB: proxies is None") 
            return False
        
        # sp: 4 篮球 29 足球
        params = (
            ('btg', '1'),
            ('c', ''),
            ('cl', '100'),
            ('d', ''),
            ('ec', ''),
            ('ev', ''),
            ('g', 'QQ=='),
            ('hle', 'false'),
            ('inl', 'false'),
            ('l', '100'),
            ('lang', ''),
            ('lg', ''),
            ('lv', ''),
            ('me', '0'),
            ('mk', '2'),
            ('more', 'false'),
            ('o', '1'),
            ('ot', '1'),
            ('pa', '0'),
            ('pimo', '0,1,2'),
            ('pn', '-1'),
            ('pv', '1'),
            ('sp', '4'),
            ('tm', '0'),
            ('v', str(int(time.time() * 1000) - 23669)),
            ('locale', 'en_US'),
            ('_', str(int(time.time() * 1000) - 1000)),
            ('withCredentials', 'true'),
        )

        response = requests.get('https://phoile.checker99.com/sports-service/sv/compact/events',
                                   impersonate="chrome110",
                                   params=params,
                                   proxies=proxies,
                                   cookies=cookies,
                                   timeout=20)
        if response.status_code != 200:
            logger.error(f"get_mids response.status_code :{response.status_code}")
            return False
        mids = []
        json_data = response.json()
        if json_data.get("l"):
            # l[0][1] l[0][2][0][2]
            if "Basketball" in json_data["l"][0][1]:
                for team_info in json_data["l"][0][2][0][2]:
                    mids.append(team_info[0])
        mids_list = mids
        logger.info("更新数据")
    except requests.RequestsError:
        pass
    except Exception as e:
        logger.error(f"get_mids:error: {e}")
        print(traceback.format_exc())


def getMatchOddsInfo2PB(u_info, mid):
    try:
        # proxies = random_proxies()
        proxies = u_info.get('proxies')
        cookies = u_info.get('cookies')
        if not cookies:
            logger.error(f"getMatchOddsInfo2PB: cookies is None") 
            return False
        if not proxies:
            logger.error(f"getMatchOddsInfo2PB: proxies is None") 
            proxies = random_proxies()
            u_info["proxies"] = proxies
        
        params = {
            'btg': '1',
            'c': '',
            'cl': '100',
            'd': '',
            'ec': '',
            'ev': '',
            'g': 'QQ==',
            'hle': 'false',
            'inl': 'false',
            'l': '100',
            'lang': '',
            'lg': '',
            'lv': '',
            'me': mid,
            'mk': '2',
            'more': 'false',
            'o': '1',
            'ot': '1',
            'pa': '0',
            'pimo': '0,1,2',
            'pn': '-1',
            'pv': '1',
            'sp': '4',
            'tm': '0',
            'v': str(int(time.time() * 1000 - 23000)),
            'locale': 'en_US',
            '_': str(int(time.time() * 1000)),
            'withCredentials': 'true',
        }

        response = requests.get('https://phoile.checker99.com/sports-service/sv/compact/events',
                                   params=params,
                                   proxies=proxies,
                                   cookies=cookies,
                                   timeout=10,
                                   # impersonate="chrome110"
                                   )
        if response.status_code == 403:
            logger.error(f"getMatchOddsInfo2PB: {response.status_code} 请求失败 {mid} account: {u_info["account"]}")
            if u_info.get("proxies"):
                del u_info["proxies"]
        if response.status_code != 200:
            logger.error(f"getMatchOddsInfo2PB: {response.status_code} 请求失败 {mid} proxies: {proxies}")
            return False

        response_data = response.json()
        if response_data["e"] and response_data["e"][3][8].get("0"):
            score_dict = fix_total_point(response_data["e"][3][8]["0"][0])
            score_info[response_data["e"][3][28]] = score_dict
        try:
            # 这里加盘口数据解析
            odd_doit = init_odds(response_data["e"])
        except:
            pass

        if response_data['ce']:
            n_match = response_data['ce'][3]
            if '角球' in n_match[1] or 'Corners' in n_match[1]:
                if n_match[28] in score_info:
                    score_info[n_match[28]].update({"角球比分": f"{n_match[9][0]}-{n_match[9][1]}"})
                    # logger.info(f"time: {datetime.datetime.now()} 更新角球比分：{score_info[n_match[28]]}")
        # print("score_info", len(score_info))
        redis_client.set("redis_play_extra_data", json.dumps(score_info))
        logger.info(f"更新mid: {mid}")
        return True
    except requests.RequestsError:
        pass
    except Exception as e:
        logger.error(f"获取mid: {mid}失败 {e}")
        print(traceback.format_exc())


def fix_total_point(odd_data):
    try:
        score_dict = {}
        if odd_data[0][2] and odd_data[0][3]:
            score_dict[f"主队大小"] = {
                odd_data[0][1]: {
                    "odd1": round(float(odd_data[0][2]), 3),
                    "odd2": round(float(odd_data[0][3]), 3)
                }
            }
        if odd_data[1][2] and odd_data[1][3]:
            score_dict[f"客队大小"] = {
                odd_data[1][1]: {
                    "odd1": round(float(odd_data[1][2]), 3),
                    "odd2": round(float(odd_data[1][3]), 3)
                }}
        return score_dict
    except:
        logger.error(f'fix_total_point: {odd_data}')



def start_mids_thread():
    while True:
        try:
            for u_info in user_info:
                if not u_info.get("cookies"):
                    continue
                threading.Thread(target=get_mids, args=(u_info,)).start()
                time.sleep(5)
        except Exception as e:
            logger.error(f"start_mids_thread {e}")

def start_odds_thread():
    global mids_list
    while True:
        try:
            if len(mids_list) == 0:
                continue
            logger.info(f"总共{len(mids_list)}场比赛")
            for mid in mids_list:
                u_info = random.choice(user_info)
                while u_info.get("cookies") is None:
                    u_info = random.choice(user_info)
                    time.sleep(0.3)
                threading.Thread(target=getMatchOddsInfo2PB, args=(u_info, mid)).start()
                time.sleep(0.1)
            time.sleep(5)
        except Exception as e:
            logger.error(f"start_odds_thread {e}")

def check_cookies():
    global user_info
    while True:
        for u_info in user_info:
            if u_info.get("cookies"):
                if not login_check(u_info):
                    del u_info["cookies"]
                    threading.Thread(target=get_authorization, args=(u_info,)).start()
        time.sleep(10)

if __name__ == '__main__':
    for info in user_info:
        threading.Thread(target=get_authorization, args=(info,)).start()
    time.sleep(20)
    threading.Thread(target=start_mids_thread).start()
    threading.Thread(target=start_odds_thread).start()
    threading.Thread(target=check_cookies).start()
    app.run(host="0.0.0.0", port=7001)
