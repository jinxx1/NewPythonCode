from functools import singledispatch


def getMax(a=None,b=None):
	error = '请输入2个int或1个list'
	if isinstance(a,int) and isinstance(b,int):
		if a>b:
			return a
		elif a<b:
			return b
		else:
			return a
	elif isinstance(a,list) and not b:
		return max(a)
	elif isinstance(b,list) and not a:
		return max(b)
	else:
		print(error)

if __name__ == '__main__':
    a = 4
    b = 9
    print(getMax(a,b))
    a=[1,2,3,4,5]
    print(getMax(a))




