import requests
from lxml import etree

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }


def GetUrl(id, cookies):
    url = 'https://las.cnas.org.cn/LAS_FQ/publish/queryOrgInfo1.action?id='+id
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        tree = etree.HTML(response.text)
        a_tags = tree.xpath('//a[@onclick]')
        nurl = ''
        for a_tag in a_tags:
            onclick_content = a_tag.get('onclick')
            if onclick_content:
                onclick_content = onclick_content.strip("();")
                url_params = onclick_content.split("_showdown('")[1]
                nurl = 'https://las.cnas.org.cn' + url_params
                print(nurl)
                return nurl
        print("No valid URL found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def GetOrtherContent(id,cookies):
    url = 'https://las.cnas.org.cn/LAS_FQ/publish/queryOrgInfo1.action?id='+id
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        tree = etree.HTML(response.text)
        contact_info = {}
        span_elements = tree.xpath('//span[@class="clabel"]')
        for span in span_elements:
            span_text = span.text
            b_element = span.xpath('./preceding-sibling::b[1]')
            if b_element:
                b_text = b_element[0].text.strip('：')  
                contact_info[b_text] = span_text  
        print(contact_info)    #[4,5,7]
        return contact_info