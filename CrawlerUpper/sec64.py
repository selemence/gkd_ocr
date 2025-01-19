import json
import requests
import websocket
import subprocess

try:
    import _thread as thread
except ImportError:
    import _thread as thread


def run_thread(ws):
    for page in range(1, 2):
        data = get_decrypt(page)
        ws.send(json.dumps(data))


def on_open(ws):
    thread.start_new_thread(run_thread, (ws,))


def get_decrypt(page_num):
    param = str(page_num)
    # result = subprocess.check_output(['node', r'sec64.js',param]).decode().split('\n')
    # return result[0]
    return param


data_num = 0


def on_message(ws, message):
    global data_num
    data_list = json.loads(message).get('data')
    print(data_list)
    for data in data_list:
        data_num += int(data.get('value'))
    print(data_num)


def on_error(ws, error):
    print(ws)
    print(error)


def on_close(ws):
    print(ws)
    print("### closed ###")


def challenge64():
    wss = "wss://www.python-spider.com/api/challenge64"
    websocket.enableTrace(True)
    # 经确定本题使用vmp加壳，先去学习
    ws = websocket.WebSocketApp(wss, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


def run():
    challenge64()


if __name__ == '__main__':
    run()
