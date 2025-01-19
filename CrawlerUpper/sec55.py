from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import requests
import json


url = "https://www.python-spider.com/api/challenge55"

def decode(encrypted_str):
    KEY = 'aiding6666666666'
    key = KEY.encode('utf-8')
    encrypted_data = base64.b64decode(encrypted_str)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8')

def run():
    data_num = 0
    for page in range(1,101):
        data = {
            "page":page,
        }
        response = requests.post(url=url,data=data)
        code_str = response.json()
        data = decode(code_str['result'])
        data_list = json.loads(data).get('data')
        data_list_num = []
        for data in data_list:
            data_list_num.append(int(data.get('value')))
            data_num += int(data.get('value'))
        print(data_list_num, page)
        print(data_num)


if __name__ =="__main__":
    run()

# function decode(str){
#     var CryptoJS = require("crypto-js");
#     var KEY = 'aiding6666666666';
#     var key = CryptoJS.enc.Utf8.parse(KEY);
#     var decrypted = CryptoJS.AES.decrypt(str, key, {
#                    // iv: iv,
#                    mode: CryptoJS.mode.ECB,
#                    padding: CryptoJS.pad.Pkcs7,
#     });
#     return decrypted.toString(CryptoJS.enc.Utf8)
# }

# decode(param)