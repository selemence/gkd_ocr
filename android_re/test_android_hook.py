import frida,sys

'''
Java.perform(function(){


})//基本构成框架
'''
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


test_t ='''
Java.perform(
    function(){
        var mainActivity = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity')
        mainActivity.onClick.implementation = function(v){
        this.onClick(v)
        console.log('owner:'+this.m.value)
        }
    }
)
'''
hook_signatures = '''
Java.perform(
    function(){
    var Signatures = Java.use('android.content.pm.Signature')
    Signatures.hashCode().implementation = function(){
        console.log('here:hashCode')
        printStack()
        return this.hashCode()//需要考虑函数是否有返回，有返回加返回没有不管
    }
    Signatures.toByteArray().implementation = function(){
        console.log('here:toByteArray')
        printStack()
        return this.toByteArray()
    }
    function printStack(){
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
    }


})
'''

test_d ='''
Java.perform(
    function(){
        console.log('im here')
        var mainActivity = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity')
        mainActivity.onClick.implementation = function(v){ //本步以及上述步骤使得程序获取到类MainActivity中的onClick方法
        console.log('owner:'+this.m.value)
        this.onClick(v)//当运行完所有需要的事情后为了保证程序不紊乱调用本体
        }
    }
)
'''

process = frida.get_usb_device(-1).attach(8724)
script = process.create_script(test_t)
script.on('message', on_message)
script.load()
sys.stdin.read()

