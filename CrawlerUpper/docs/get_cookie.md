如果出现数据在一段时间内能够通过API获取，随着时间推移API失效其大概率是cookie失效，可以尝试打页面脚本断点然后根据hook获取相应的cookie生成位置再获取cookie生成逻辑，以下就是hook代码，在hook住后向上翻堆栈即可

> 



```javascript
(function(){
    Object.defineProperty(document, 'cookie', {
        set:function(val){
            debugger
            return val
        }
    })
})();

```
