import requests

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://las.cnas.org.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://las.cnas.org.cn/LAS_FQ/publish/lab/checkLabObjListView.jsp?baseInfoId=00bd4375e7364b22bf025df6b52df0db&enstart=0&blueTooth=0&type=abilityL1&orgEnOrCh=Ch&certUpdateTs=2024-11-08&validate=2030-11-29&attactdate=',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

def get_base_info_id(url):
    if url is None:
        return None
    else:
        query_start = url.find('?')
        if query_start == -1:
            return None 
        query_string = url[query_start + 1:]
        pairs = query_string.split('&')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                if key == 'baseInfoId':
                    return value
        return None


def GeneContent(url,cookies,orther):
    baseinfoId = get_base_info_id(url)
    data = {
        '$': '',
        'baseinfoId': baseinfoId,
        'type': 'L1',
        'enstart': '0',
        'blueTooth': '0',
        '__checkbox_chcckName': 'true',
        'checkBoxEck': '0',
        }
    response = requests.post('https://las.cnas.org.cn/LAS_FQ/publish/queryPublishLCheckObj.action', headers=headers, cookies=cookies, data=data).json()
    html_table = '<p>联系电话：13530227809</p>\n'
    html_table += f'<p>联系电话：{orther["联系电话"]}</p>\n'
    html_table += f'<p>电子邮箱：{orther["电子邮箱"]}</p>\n'
    html_table += f'<p>单位地址：{orther["单位地址"]}</p>\n'
    if baseinfoId ==None:
        html_table +='<p>此处暂时没有内容<p>'
        return html_table
    else:
        html_table += "<table border='1'>\n"
        html_table += "<tr><th>序号</th><th>材料类型</th><th>测试项目</th><th>测试标准</th><th>备注</th><th>状态</th></tr>\n"

        # 填充表格数据
        for index, item in enumerate(response['data'], start=1):
            html_table += "<tr>"
            html_table += f"<td>{index}</td>"
            html_table += f"<td>{item['objCh']}</td>"
            html_table += f"<td>{item['paramCh']}</td>"
            html_table += f"<td>{item['stdDesc']}</td>"
            html_table += f"<td>{item['limitCh']}</td>"
            html_table += "</tr>\n"

        # 结束HTML表格
        html_table += "</table>"
        return html_table

  