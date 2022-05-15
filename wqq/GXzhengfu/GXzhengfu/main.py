from scrapy.cmdline import execute
top_drib = int(input("请输入重复数：\n"))
spiders = [
    'scrapy crawl GXzhengfu'
]
if __name__ == '__main__':
    execute(spiders[0])
