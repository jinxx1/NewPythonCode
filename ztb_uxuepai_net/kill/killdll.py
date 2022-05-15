import psutil, os, time, datetime, requests


def main():
	brow = requests.get(url='http://120.79.3.69:8050/')
	if brow.status_code != 200:
		print('Please contact the jinxiao')
		return None

	ps = psutil.pids()
	num = 0
	for pi in ps:
		p = psutil.Process(pi)
		if p.name().find("sysupdate") == 0:
			pidnum = p.pid
			num += 1
			try:
				os.system("kill {}".format(pidnum))
			except Exception as info:
				print(info)

		if p.name().find("networkservice") == 0:
			pidnum = p.pid
			num += 1
			try:
				os.system("kill {}".format(pidnum))
			except Exception as info:
				print(info)
		if p.name().find("sysguard") == 0:
			pidnum = p.pid
			num += 1
			try:
				os.system("kill {}".format(pidnum))
			except Exception as info:
				print(info)

	if num == 0:
		print(datetime.datetime.now())
	else:
		print('{} viruses were found--------'.format(str(num)), datetime.datetime.now())

	return True
if __name__ == '__main__':
    main()