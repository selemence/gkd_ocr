import requests

url = 'https://www.python-spider.com/challenge/3'
headers={
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


def run():
    for page in range(1,2):
        data = {
            'page': page,
        }
        # result = pass
        cookies = {
            'sessionid' : '7rj0w9hchoxcfb1iu817z8w2xudznbwi',
            'm' : result,
        }
        response = requests.post(url=url,headers=headers,cookies=cookies,data=data)
        print(response.text)
        
        
if __name__ == '__main__':
    run()
    
    # def sum(Y,Z):
    #   return Y+Z
    # def func(Y,Z):
    #   return Y(Z)
    #  document.cookie= sum(sum(sum(sum(m + '', '='), A[$b('\x30\x78\x35\x31', '\x31\x6a\x73\x35') + '\x71\x42'](V, Y)), '\x7c'), Y) + A[$b('\x30\x78\x31\x62', '\x28\x35\x72\x26') + '\x42\x50'];
    #    document['coo'+ "kie"] = A[$b("0x42", "6)pn") + "Bj"](A[$b("0xf3", "VyjD") + "Xr"](A[$b("0x1e", "IYO8") + "xT"](A[$b("0x112", "#lO)") + "fC"]("m" + A[$b("0x86", "jovN") + "xR"](M), "="), A[$b("0x51", "1js5") + "qB"](V, Y)), "|"), Y) + A[$b("0x1b", "(5r&") + "BP"];