def cutpid():
    import psutil, os
    ps = psutil.pids()
    for pi in ps:
        p = psutil.Process(pi)
        if p.name().find("goon=no") > 0:
            try:
                os.system("kill {}".format(p.pid))
            except Exception as info:
                pass
if __name__ == '__main__':
    cutpid()