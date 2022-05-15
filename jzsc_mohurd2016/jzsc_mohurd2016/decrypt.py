import base64
from Crypto.Cipher import AES
import json
import pprint

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
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypt_bytes = cipher.decrypt(bytes.fromhex(content))
        result = str(decrypt_bytes, encoding='utf-8')
        result = cls._pkcs7unpadding(result)
        return result

if __name__ == '__main__':



    aes = AESDecrypt()
    decDate = aes.decrypt(word)
    getdate = json.loads(decDate)
    import pprint
    pprint.pprint(getdate)


