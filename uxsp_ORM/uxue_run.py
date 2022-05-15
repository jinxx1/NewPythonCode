import os, sys
import asyncio


async def rundef(num):
	for i in range(10):
		await asyncio.sleep(num)
		print(num)
	# os.system("python mysqlORM.py {}".format(num))




async def main():
	task1 = asyncio.create_task(rundef(1))
	task2 = asyncio.create_task(rundef(2))
	task3 = asyncio.create_task(rundef(3))
	task4 = asyncio.create_task(rundef(4))
	await task1
	await task2
	await task3
	await task4


if __name__ == '__main__':
	asyncio.run(main())
