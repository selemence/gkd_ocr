var k = require('crypto-js');
const args = process.argv;
const c_res = args[2];

X = c_res.slice(0,8)
l = c_res

function I(X, l) {
    q = k['enc']['Utf8']['parse'](X)
  , v = k['DES']['decrypt'](l, q, {
        'mode': k['mode']['ECB'],
        'padding': k['pad']['Pkcs7']
    });
     datas = v['toString'](k['enc']['Utf8']);
    console.log(datas)
    return datas;
}

I(X,l)