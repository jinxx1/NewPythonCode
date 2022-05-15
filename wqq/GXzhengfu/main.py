from scrapy.cmdline import execute


top_drib = int(input("请输入重复数：\n"))
spiders = [
    'scrapy crawl GXspider'
]
if __name__ == '__main__':
    for i in spiders:
        execute(i.split())
