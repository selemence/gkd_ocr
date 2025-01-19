#  var list = {
#             "page": String(num),
#             "token": btoa(num),
#         };
#      5076135
import requests
import base64

url = "https://www.python-spider.com/api/challenge54"


def btoa(data):
    code = base64.b64encode(data.encode('utf8'))
    res = str(code,'utf-8')
    return res
    
def send_request(page):
    token = btoa(str(page))
    datas = {
        'page':page,
        'token':token,
    }
    headers = {
   'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    cookies = {
        'sessionid': 'bh6qvnseejgodmn27j54u3puqa2d0iis'
    }
    session = requests.Session()
    session.headers.clear()
    session.headers.update(headers)
    session.headers = headers
    response = session.post(url,cookies=cookies,data=datas)
    print(response)
    return response.json()  

def run():
    total_sum = 0
    for page in range(1,101):
        response_data = send_request(page)
        data_list = response_data['data']
        for item in data_list:
            total_sum += int(item['value'])
    print(f"The total sum of all values is: {total_sum}")


if __name__ == '__main__':
    run()