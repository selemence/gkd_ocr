from curl_cffi import requests

url = 'https://www.python-spider.com/api/challenge22'
cookies = {
    'sessionid' : '3poojk0tc8zd27id7o4xj5es00z54d5k',
    '__yr_token__' : 'b301cDC5tEGhreXEWfA1OU3A4Y0cjY2olYVMObURzQ09jQit0T1d6bAoGYX5SRH8eWhlHSF9LRgg5ZzECY0ljC0RzaB8bG0MgQXN9CC8cLnMaYkxiGhEYB0gUWAZYF3ZrXAZPABUMG3kJWQNBYRY=' #此处为障眼法，下次可大胆些
}

def run():
    total_sum = 0
    for page in range(1,101):
        data = {'page' : page}
        response = requests.post(url=url, impersonate="Chrome101",cookies=cookies,data=data).json()
        print(response)
        page_data = response['data']
        num_list = sum([int(i['value']) for i in page_data])
        total_sum += num_list
    print(total_sum)

if __name__ == "__main__":
    run()