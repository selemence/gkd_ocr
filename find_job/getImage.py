import requests

cookies = {
    '__jsluid_s': 'ddbf2faf435e2e6e3873cfd05ddd3fcd',
    '__jsl_clearance_s': '1734397082.247|0|VZ%2FnK5bE65jO7u95xQX61TTgcZI%3D',
    'JSESSIONID': '00001OBnY0UAgV4Y2bwBIVM3hPU:1aj22nhv3',
    'SF_cookie_3': '24923034',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://las.cnas.org.cn/LAS_FQ/publish/externalQueryL1.jsp',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


response = requests.get('https://las.cnas.org.cn/LAS_FQ/verify/getValidateCode.action', headers=headers, cookies=cookies)
print(response)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://las.cnas.org.cn/LAS_FQ/verify/getValidateCode.action?fleshCode=0.5672512669502738', headers=headers, cookies=cookies)
