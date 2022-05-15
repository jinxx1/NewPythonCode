import os,time,sys



try:
    if sys.argv[1] == '0':
        while 1:
            os.system('scrapy crawlall -a breakpoint=False')
            time.sleep(60)
    else:
        while 1:
            os.system('scrapy crawlall -a breakpoint=True')
            time.sleep(60)
except IndexError:
    print('-------------------------------------------------------------------------------------------')
    print(' ')
    print('没有正确填写参数。请在   python runScrapy.py   后面 加空格 填写一个数字')
    print(' ')
    print('数字 0  为  禁止  断点续传。其他任意数字为默认可以 ')
    print(' ')
    print('如：\"python runScrapy.py 0\"   此命令为 禁止 进行断点续传，注意空格。如果 禁止 必须用0')
    print(' ')
    print('如：\"python runScrapy.py 1\"   此命令为 允许 进行断点续传，注意空格。1可以是任意数字')
    print(' ')
    print('-------------------------------------------------------------------------------------------')



