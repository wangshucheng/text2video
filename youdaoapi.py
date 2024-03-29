import json
from Crypto.Cipher import AES
import hashlib
import base64
from Crypto.Util.Padding import unpad
import time
import requests
import json
class Trans:
    def decrypt(decrypt_str):
        key = "ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl"
        iv = "ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4"
 
        key_md5 = hashlib.md5((key).encode('utf-8')).digest()
        iv_md5 = hashlib.md5((iv).encode('utf-8')).digest()
        # print('key_md5：', key_md5)
        # print('iv_md5：', iv_md5)
        # print()
        aes = AES.new(key=key_md5, mode=AES.MODE_CBC, iv=iv_md5)
 
        code = aes.decrypt(base64.urlsafe_b64decode(decrypt_str))
        return unpad(code, AES.block_size).decode('utf8')
 
 
    def get_data(translation_words):
        url = 'https://dict.youdao.com/webtranslate'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=379056539.64209586; OUTFOX_SEARCH_USER_ID=-380628258@222.182.116.19',
            'Host': 'dict.youdao.com',
            'Origin': 'https://fanyi.youdao.com',
            'Referer': 'https://fanyi.youdao.com/',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
 
        # 'ts':   '1680404913064',  ==> 13位 当前时间戳
        # fsdsogkndfokasodnaso 固定值
 
        ts = str(int(time.time() * 1000))
        str_sign = f"client=fanyideskweb&mysticTime={ts}&product=webfanyi&key=fsdsogkndfokasodnaso"
        sign = hashlib.md5((str_sign).encode('utf-8')).hexdigest()
 
        # print('------------------------sign------------------------')
        # print('sign为：', sign, end='\n\n')
        form_data = {
            'i': translation_words,
            'from': 'auto',
            'to': '',
            'sign': sign,
            'dictResult': 'true',
            'keyid': 'webfanyi',
            'client': 'fanyideskweb',
            'product': 'webfanyi',
            'appVersion': '1.0.0',
            'vendor': 'web',
            'pointParam': 'client,mysticTime,product',
            'mysticTime': ts,
            'keyfrom': 'fanyi.web',
        }
 
        res = requests.post(url=url, headers=headers, data=form_data).text
 
        # print('------------------------返回的数据密文------------------------')
        # print(res, end='\n\n')
        return res
   
    def fnayi(pre_words):
        translation_words = pre_words
        # translation_words = input("请输入要翻译的：")
        decrypt_str = Trans.get_data(translation_words)
        end_code = Trans.decrypt(decrypt_str)
        # print('------------------------解密后的数据密文------------------------')
        # print(end_code, end='\n\n')
        json_data = json.loads(end_code)
 
        # print('-------------------------有道翻译-------------------------')
        # print('翻译前：', translation_words)
        # print('翻译后：', json_data['translateResult'][0][0]['tgt'])
        return json_data['translateResult'][0][0]['tgt']
 
 
if __name__ == "__main__":
    # print(translate_to_english("我是中国人"))
    
    test_str="我是中国人"
    result=Trans.fnayi(test_str)
    print(result)