# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GgzyItem(scrapy.Item):

    # ztbRawInfo 表名称（文章信息存储表）
    subclass = scrapy.Field()  # 子类型
    site = scrapy.Field()  # 来源站点,域名
    page_url = scrapy.Field()  # 链接地址
    title = scrapy.Field()  # 标题
    issue_time = scrapy.Field()  # 发布时间
    creation_time = scrapy.Field()  # 抓取开始时间
    end_time = scrapy.Field()  # 抓取结束时间
    city_name = scrapy.Field()  # 市
    craw_status = scrapy.Field()

    minor_business_type = scrapy.Field()  # 业务细类
    money = scrapy.Field()  # 项目金额
    # --------------------------------------------------------------------------

    # ztbRawInfoContent 表名称（内容存储表）
    content = scrapy.Field()  # 公告内容
    raw_data_id = scrapy.Field()  # 公告内容
    # --------------------------------------------------------------------------

    # ztbInfoAttachment 表名称（附件存储表）
    attchment = scrapy.Field()
    info_id = scrapy.Field()
    raw_id = scrapy.Field()  # 公告内容
    download_url = scrapy.Field()  # 原始网站的附件下载地址
    name = scrapy.Field()  # 文件对应的名称,如文件名为123.xls,name为广州招标

    # --------------------------------------------------------------------------
    # ztb_raw_info_attached 表名称（附件存储表）
    # 业务类型: 入附加数据表, key: business_type, value: 工程建设 / 政府采购 / 等等
    # 信息类型: 入附加数据表, key: purchase_type, value: 招标 / 资审公告 / 开标记录 / 等等
    # 行业: 入附加数据表, key: industry, value: 农业 / 林业 / 等等
    # 省分: 入附加数据表, key: province_name, value: 湖南 / 湖北 / 等等
    # 来源平台: 入附加数据表, key: source, value: 平凉市电子交易系统 / 等等

    business_type = scrapy.Field()  # 业务大类
    purchase_type = scrapy.Field()  # 采购方式
    province_name = scrapy.Field()  # 省
    source = scrapy.Field()         # 来源平台
    industry = scrapy.Field()       # 行业
