def mkdir(path):
	import os
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)
if __name__ == '__main__':
	pass
