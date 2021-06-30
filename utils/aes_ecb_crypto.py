import base64
import json

from Crypto.Cipher import AES

'''
采用AES对称加密算法
'''


class AesEncry():  # aes秘钥

    def __init__(self, key, mode, vi=None):
        self.key = key
        self.mode = mode
        self.vi = vi

    def encrypt(self, data):
        # data = json.dumps(data)
        if self.mode == "ECB":
            mode = AES.MODE_ECB
            padding = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
            cryptos = AES.new(self.key, mode)
            cipher_text = cryptos.encrypt(padding(str(data)).encode("utf-8"))
            return base64.b64encode(cipher_text).decode("utf-8")

    def decrypt(self, data):
        cryptos = AES.new(self.key, AES.MODE_ECB)
        decrpytBytes = base64.b64decode(data)
        meg = cryptos.decrypt(decrpytBytes).decode('utf-8')
        return meg[:-ord(meg[-1])]


if __name__ == "__main__":

    key = "e10adc3949ba59abbe56e057f20f883e"
    encrypto_str = "13184560031"
    decrypto_str = "UQz/6nEF0WaF4TuBwWwTGA=="
    aescryptor = AesEncry(key, "ECB")
    d_print = aescryptor.encrypt(decrypto_str)
    # d_print = aescryptor.decrypt(decrypto_str)
    print(d_print)
