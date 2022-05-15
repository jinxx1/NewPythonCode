import zipfile
import random
import time
import sys


class MyIterator():
    # 单位字符集合
    letters = "abcdefghijklmnopqrstuvwxyz012345678ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    min_digits = 0
    max_digits = 0

    def __init__(self, min_digits, max_digits):
        # 实例化对象时给出密码位数范围，一般4到10位
        if min_digits < max_digits:
            self.min_digits = min_digits
            self.max_digits = max_digits
        else:
            self.min_digits = max_digits
            self.max_digits = min_digits

    # 迭代器访问定义
    def __iter__(self):
        return self

    def __next__(self):
        rst = str()
        for item in range(0, random.randrange(self.min_digits, self.max_digits + 1)):
            rst += random.choice(MyIterator.letters)
        return rst


def extract():
    start_time = time.time()
    zfile = zipfile.ZipFile(r"D:\下载_软件\《从芯片到云端：Python 物联网全栈开发实践》高清PDF+源码+延伸阅读+刘凯\《从芯片到云端：Python 物联网全栈开发实践》高清PDF+源码+延伸阅读+刘凯\《从芯片到云端：Python 物联网全栈开发实践》高清PDF+源码+延伸阅读+刘凯.zip")
    for p in MyIterator(4,10):
        try:
            zfile.extractall(path=".", pwd=str(p).encode('utf-8'))
            print("the password is {}".format(p))
            now_time = time.time()
            print("spend time is {}".format(now_time - start_time))
            sys.exit(0)
        except Exception as e:
            print(e)
            print(p)
            print('------------------')


if __name__ == '__main__':
    count = 1
    for n in range(1,11):
        aa = 62 ** n
        count = count * aa
    print(count)


    exit()
    extract()