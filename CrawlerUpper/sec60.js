const args = process.argv;
const param = args[2];

var CryptoJS = require('crypto-js')

// 3DES加密，page必须为字符串
function get_data(page) {
    var d = CryptoJS.enc.Utf8.parse('aiding88'),
        D = CryptoJS.TripleDES.encrypt(page, d, {
            'mode': CryptoJS.mode.ECB,
            'padding': CryptoJS.pad.Pkcs7
        })
    return D.toString()
}
_url = get_data(param)
console.log(_url)