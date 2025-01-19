import requests
def LoadContent(data,content):
    
    cookies = {
        'PHPSESSID': 'uhtsnss17a8kf1hpuhleasd4c0',
        'admin_lang': 'cn',
        'lang_info': 'think%3A%7B%22lang_title%22%3A%22%25E7%25AE%2580%25E4%25BD%2593%25E4%25B8%25AD%25E6%2596%2587%22%2C%22lang_url%22%3A%22%252F%22%2C%22lang_logo%22%3A%22%252Fpublic%252Fstatic%252Fcommon%252Fimages%252Flanguage%252Fcn.gif%22%7D',
        'home_lang': 'cn',
        'ENV_UPHTML_AFTER': '%7B%22seo_uphtml_after_home%22%3A0%2C%22seo_uphtml_after_channel%22%3A0%2C%22seo_uphtml_after_pernext%22%3A%221%22%7D',
        'users_id': '10',
        'workspaceParam': 'welcome%7CIndex',
        'ENV_GOBACK_URL': '%2Flogin.php%3Fm%3Dadmin%26c%3DArticle%26a%3Dindex%26channel%3D1%26lang%3Dcn',
        'ENV_LIST_URL': '%2Flogin.php%3Fm%3Dadmin%26c%3DArticle%26a%3Dindex%26lang%3Dcn',
        'ENV_IS_UPHTML': '0',
    }
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://pvoc.xbaohui.com/login.php',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    }

    url = 'http://pvoc.xbaohui.com/login.php?m=admin&c=Article&a=add&lang=cn'
    data = {
    'title': data,  #采集到的数据
    'subtitle': '',
    'typeid': '99', #根据实际标题
    'jumplinks': '',
    'tags': '',
    'province_id': '0',
    'city_id': '',
    'area_id': '',
    'litpic_local': '',
    'litpic_remote': '',
    'restric_type': '0',
    'arc_level_id': '1',
    'users_price': '',
    'part_free': '0',
    'size': '1024',
    'addonFieldExt[content]': content, #内容
    'addonFieldExt[content_ey_m]': '',
    'seo_title': '',
    'seo_keywords': '',
    'seo_description': '',
    'author': '\u5C0F\u7F16',
    'origin': '\u7F51\u7EDC',
    'click': '500',
    'arcrank': '0',
    'add_time': '2024-12-18 15:57:54',
    'tempview': 'view_article.htm',
    'type_tempview': 'view_article.htm',
    'htmlfilename': '',
    'free_content': '',
    'gourl': '',
    'editor_addonFieldExt': 'content_ey_m,content'
    }
    response = requests.post(url,cookies=cookies,headers=headers,data=data)

    if response.status_code == 201:
        print('文章已计划发布。')
    else:
        print('发布失败：', response.content)
        














