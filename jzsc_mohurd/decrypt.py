import base64
from Crypto.Cipher import AES

import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

# def reaEncrypt(strs):
#     pubkey =

# rsa加密
def rsaEncrypt(strs):
    # 生成公钥、私钥
    # (pubkey, privkey) = rsa.newkeys(512)
    pubkey='MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfXfMzgg4m5RRLg2vcrYBFN4sBhE1VtW1sBkXxC5wtCRaOZv0kudk9CIQfU6c+eEaaZKUnygxHWdSqdwURCE0IKgLcolXF+RHmu/rl977FfjRg9pAkBg5z05PfHDqWqkIsqX0iRaSP31BUZOgtwafbiBv2dBvRBMdq03ty4q8OQQIDAQAB'
    pubkey = rsa.PublicKey(int(pubkey,16),int("010001",16))
    crypto = rsa.encrypt(bytes(strs,encoding='utf-8'),pubkey)

    return (crypto, pubkey)





class AESDecrypt:
    iv = '0123456789ABCDEF'
    key = 'jo8j9wGw%6HbxfFn'
    @classmethod
    def _pkcs7unpadding(cls, text):
        # 处理PKCS7
        length = len(text)
        unpadding = ord(text[length-1])
        return text[0:length-unpadding]

    @classmethod
    def decrypt(cls, content):
        # AES解密cbc，填充pkcs7
        key = bytes(cls.key, encoding='utf-8')
        iv = bytes(cls.iv, encoding='utf-8')
        cipher = AES.new(iv=iv, mode=AES.MODE_CBC, key=key)
        decrypt_bytes = cipher.decrypt(bytes.fromhex(content))
        result = str(decrypt_bytes, encoding='utf-8')
        result = cls._pkcs7unpadding(result)
        return result


if __name__ == '__main__':

    a1 = 'dd'
    print(aaa(a1))

    str, pk = rsaEncrypt('kHEaCZnifhirMMH3')
    print("加密后密文：",str)

    exit()
    # DetailList是www.cnpcbidding.com/cms/pmsbidInfo/listPageOut的返回值

    DetailList = {"encrypted":"XzotyL32kNyr9pTmMNRhyctXY2gqH3g71p++UwS+V1GPhW/x51mtLo5m5Dl0ZVcM4jQ+aQbwCCfL\r\ncnxKp7m/Mln0gfLnbPcwUTRiEYdL58td3U8UghheibOCNUMktinJNP2hF71lKITgBVber+9rp2o/\r\nxdSIgW7AE0dT/YaIdMM=\r\n","requestData":"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"}

    aes = AESDecrypt()
    a= aes.decrypt(DetailList['requestData'])
    import json
    aa = json.loads(a)
    import pprint
    pprint.pprint(aa)