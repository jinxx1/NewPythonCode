import psutil,os,time,datetime
def main():
    ps = psutil.pids()
    num = 0
    for pi in ps:
        p = psutil.Process(pi)
        if p.name().find("sysupdate") == 0:
            pidnum = p.pid
            num += 1
            print('发现sysupdate:',pidnum)
            try:
                os.system("kill {}".format(pidnum))
                print("已经关闭sysupdate进程:", pidnum)
            except Exception as info:
                print('无法关闭sysupdate进程')
                print(info)

        if p.name().find("networkservice") == 0:
            pidnum = p.pid
            num += 1
            print('发现networkservice:',pidnum)
            try:
                os.system("kill {}".format(pidnum))
                print("已经关闭networkservice进程:", pidnum)
            except Exception as info:
                print('无法关闭networkservice进程')
                print(info)

        if p.name().find("sysguard") == 0:
            pidnum = p.pid
            num += 1
            print('发现sysguard:',pidnum)
            try:
                os.system("kill {}".format(pidnum))
                print("已经关闭sysguard进程:", pidnum)
            except Exception as info:
                print('无法关闭sysguard进程')
                print(info)

        # if p.name().find("sendmail") == 0:
        #     pidnum = p.pid
        #     print('sendmail:',pidnum)
        #     try:
        #         os.system("kill {}".format(pidnum))
        #         print("已经关闭sendmail进程:", pidnum)
        #     except Exception as info:
        #         print('无法关闭sendmail进程')
        #         print(info)

        # if p.name().find("postdrop") == 0:
        #     pidnum = p.pid
        #     print('postdrop:',pidnum)
        #     try:
        #         os.system("kill {}".format(pidnum))
        #         print("已经关闭postdrop进程:", pidnum)
        #     except Exception as info:
        #         print('无法关闭postdrop进程')
        #         print(info)

    if num == 0:
        print(datetime.datetime.now())
    else:
        print('本次扫描发现{}个病毒进程--------'.format(str(num)),datetime.datetime.now())



if __name__ == '__main__':

    while True:
        try:
            main()
            time.sleep(5)
        except Exception as ff:
            print(ff)







