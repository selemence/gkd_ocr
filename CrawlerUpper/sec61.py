import websocket
import subprocess


param ='1'
result = subprocess.check_output(['node', r'github_sec61.js',param]).decode().split('\n')

print(result)










# result = subprocess.check_output(['node', r'sec61.js']).decode().split('\n')
#  本题由于个人能力暂时无法查找到错误源头，后续浏览器调试           var r = i.MD5 = O.extend({
# TypeError: Cannot read properties of undefined (reading 'extend')
#     at D:\VsCodeProject\sec61.js:1084:35
#     at D:\VsCodeProject\sec61.js:1231:14
#     at D:\VsCodeProject\sec61.js:1063:56
#     at 13 (D:\VsCodeProject\sec61.js:1069:11)
#     at k (D:\VsCodeProject\sec61.js:188:23)
#     at D:\VsCodeProject\sec61.js:190:26
#     at D:\VsCodeProject\sec61.js:1018:171
#     at 11 (D:\VsCodeProject\sec61.js:1024:11)
#     at k (D:\VsCodeProject\sec61.js:188:23)
#     at D:\VsCodeProject\sec61.js:190:26

# Node.js v20.17.0
# Traceback (most recent call last):
#   File "d:/VsCodeProject/sec61.py", line 5, in <module>
#     result = subprocess.check_output(['node', r'sec61.js']).decode().split('\n')
#   File "C:\Users\allright\AppData\Local\Programs\Python\Python38\lib\subprocess.py", line 411, in check_output
#     return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
#   File "C:\Users\allright\AppData\Local\Programs\Python\Python38\lib\subprocess.py", line 512, in run
#     raise CalledProcessError(retcode, process.args,
# subprocess.CalledProcessError: Command '['node', 'sec61.js']' returned non-zero exit status 1.