# from fontTools.ttLib import TTFont


# # 读取woff文件
# font = TTFont(r'./aiding.woff')
# font.saveXML(r'./woff_data.xml')
import requests
from xml.dom.minidom import parse
dom = parse(r'./woff_data.xml')
# 获取文档元素对象
data = dom.documentElement
# 获取 <map code="0xf0d6" name="unif0d6"/> 中的code与对应name
maps = data.getElementsByTagName('map')
codeName_dict = {}
for m in maps:
    code = m.getAttribute("code")
    cname = m.getAttribute("name")
    codeName_dict[code] = cname
    
# 获取 <GlyphID id="8" name="unif0d6"/> 中的id与对应name
GlyphOrder = data.getElementsByTagName('GlyphID')
nameCId_dict = {}
for g in GlyphOrder:
    cid = g.getAttribute("id")
    if len(cid) > 1:  # xml中的10在网页中显示为0
        cid = cid[-1]
    cname = g.getAttribute("name")
    nameCId_dict[cname] = cid    


url = 'https://www.python-spider.com/api/challenge12'
total_sum = 0
for page in range(1,101):   
    payload = {"page": page}
    res = requests.post(url, data=payload).json()
    datas = res.get('data')
    for d in datas:
        value = d.get('value')
        vstr = value.split(' ')[:-1]
        vs = ''
        for v in vstr:
            cname = codeName_dict.get(v.replace('&#', '0'))
            cvalue = nameCId_dict.get(cname)
            vs += cvalue
        total_sum +=int(vs)
print(total_sum)