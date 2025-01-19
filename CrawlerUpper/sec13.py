# import requests
# import base64
# import json
# from fontTools.ttLib import TTFont
# from io import BytesIO

# session = requests.Session()
# headers={
#     'method': 'POST',
#     'authority': '',
#     'scheme': 'https',
#     'path': '/api/challenge24',
#     'sec-ch-ua':'"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
#     'accept':'application/json, text/javascript, */*; q=0.01',
#     'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
#     'x-requested-with':'XMLHttpRequest',
#     'sec-ch-ua-mobile':'?0',
#     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
#     'sec-ch-ua-platform':'"Windows"',
#     'origin':'',
#     'sec-fetch-site':'same-origin',
#     'sec-fetch-mode':'cors',
#     'sec-fetch-dest':'empty',
#     'referer':'',
#     'accept-encoding':'gzip, deflate, br',
# }
# cookies = {
#     'sessionid': 'ycgq6ll5jfie50vnou859v03om19yqkk'
# }


# def process_font_data(ttf_b64):
#     ttf_data = base64.b64decode(ttf_b64)
#     font = TTFont(BytesIO(ttf_data))

#     # Getting cmap (similar to <map code="0xf0d6" name="unif0d6"/> code and name)
#     codeName_dict = {hex(k): v for k, v in font.getBestCmap().items()}

#     # Getting GlyphOrder (similar to <GlyphID id="8" name="unif0d6"/> id and name)
#     nameCId_dict = {name: str(i) if i != 10 else '0' for i, name in enumerate(font.getGlyphOrder())}

#     return codeName_dict, nameCId_dict

# url = 'https://www.python-spider.com/api/challenge13'  # 修正URL
# total_sum = 0
# for page in range(1,101):   
#     payload = {"page": page}
#     session.headers.clear()
#     session.headers.update(headers)
#     res = session.post(url,headers=headers, cookies=cookies,data=payload,proxies={}) 
#     res = json.loads(res.text)
#     datas = res.get('data')
#     for d in datas:
#         value = d.get('value')
#         vstr = value.split(' ')[:-1]
#         vs = ''
#         for v in vstr:
#             ttf = res.get("woff") 
#             codeName_dict,nameCId_dict = process_font_data(ttf)
#             cname = codeName_dict.get(v.replace('&#', '0'))
#             cvalue = nameCId_dict.get(cname)
#             vs += cvalue
#         total_sum +=int(vs)

# print(total_sum)


from fontTools.ttLib import TTFont
import requests


def font_value(key):
    font = TTFont('./aiding.woff')
    font.saveXML('./movie.xml')
    font_dict = {}
    i = 1
    for font_u_nie in font['post'].extraNames[:-1]:
        font_dict[font_u_nie] = i
        i += 1
    font_dict[font['post'].extraNames[-1]] = 0
    return font_dict[key]


def get_ttf(woff):
    import base64
    ttf_name = 'aiding'
    with open('./aiding.ttf', 'wb') as f:
        f.write(base64.b64decode(woff))
    with open('./aiding.woff', 'wb') as f:
        f.write(base64.b64decode(woff))
    return ttf_name


def challenge13(page):
    url = "https://www.python-spider.com/api/challenge13"
    payload = f"page={page}"
    session = requests.session()
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    session.headers = headers
    response = session.request("POST", url, data=payload)
    print(response)
    return response.json()


def run():
    data_num = 0
    for page in range(1, 101):
        response_json = challenge13(page)
        data_list = response_json.get('data')
        woff = response_json.get('woff')
        get_ttf(woff)
        for data in data_list:
            data_value_list = data.get('value').split(' ')[:-1]
            data_num_join = ''
            for data_value in data_value_list:
                data_value_num = font_value(data_value.replace('&#x', 'uni'))
                data_num_join += str(data_value_num)
            data_num += int(data_num_join)
    print(data_num)


if __name__ == '__main__':
    run()