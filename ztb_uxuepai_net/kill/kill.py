from killdll import main
import time
if __name__ == '__main__':

    while True:
        try:
            a = main()
            if not a:
                print('Please contact the jinxiao')
                break
            else:
                time.sleep(15)
        except Exception as ff:
            print(ff)