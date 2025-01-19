import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

iCity_test = '''
function hook1(clz) {
    // 示例：hook 类中的一个方法
    clz.a.implementation = function() {
        console.log("Method a called");
        // 调用原方法
        return this.a.apply(this, arguments);
    };
}

Java.perform(function() {
    Java.enumerateClassLoaders({
        onMatch: function(loader) {
            try {
                var myClass = Java.use(loader, "com.iCitySuzhou.suzhou001.p187d.C1669d");
                console.log("Class loaded: " + myClass);
                hook1(myClass);
                return "stop"; // 停止进一步匹配
            } catch (e) {
                console.log("Error loading class with loader: " + loader);
                console.log("Error: " + e.message);
                console.log("Stack trace: " + e.stack);
            }
        },
        onComplete: function() {
            console.log("Done");
        }
    });
});
'''

process = frida.get_usb_device(-1).attach(8389)
script = process.create_script(iCity_test)
script.on('message', on_message)
script.load()
input("Press Enter to exit...\n")