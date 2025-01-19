function randomString(len) {
    len = len || 32;
    var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz123456789=+-';
    /****默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1****/
    var maxPos = $chars.length;
    var pwd = '';
    for (i = 0; i < len; i++) {
        pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
    }
    return pwd;
}
seed = randomString(32);


function b(c, d) {
    c = c - 0x0;
    var e = a[c];
    if (b['bSTWem'] === undefined) {
        var f = function(h) {
            var i = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='
              , j = String(h)['trimEnd']('=');
            var k = '';
            for (var l = 0x0, m, n, o = 0x0; n = j['charAt'](o++); ~n && (m = l % 0x4 ? m * 0x40 + n : n,
            l++ % 0x4) ? k += String['fromCharCode'](0xff & m >> (-0x2 * l & 0x6)) : 0x0) {
                n = i['indexOf'](n);
            }
            return k;
        };
        b['CkzzXs'] = function(h) {
            var j = f(h);
            var k = [];
            for (var l = 0x0, m = j['length']; l < m; l++) {
                k += '%' + ('00' + j['charCodeAt'](l)['toString'](0x10))['slice'](-0x2);
            }
            return decodeURIComponent(k);
        }
        ,
        b['DXfPIG'] = {},
        b['bSTWem'] = !![];
    }
    var g = b['DXfPIG'][c];
    return g === undefined ? (e = b['CkzzXs'](e),
    b['DXfPIG'][c] = e) : e = g,
    e;
};

function bw(cu, cv) {
    var cw = {
        'yRCsB': function(cB) {
            return cB();
        },
        'hOYXs': function(cB) {
            return cB();
        },
        'LvSzb': b('0x4e5'),
        'dVmHH': function(cB, cC) {
            return cB(cC);
        }
    }, cx = new Date()['getTime'](), cy, cz, cA;
    return cA = cu,
    cw['yRCsB'](bV),
    cy = c0(cA, cv),
    bU(cA, cv),
    c8(this[b('0x18c')]),
    cw[b('0x782')](ca),
    cz = bB(cy, cA),
    bK(cz, cA, this[b('0x5e2')]),
    ABC[cw['LvSzb']]['t'] = new Date()['getTime']() - cx,
    cw['dVmHH'](bI, ax);
}


document.cookie = '__yr_token__=' + bw(seed, parseInt(new Date().getTime()) + (480 + (new Date).getTimezoneOffset()) * 60 * 1e3) + ';path=/'
