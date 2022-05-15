# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShangqingItem(scrapy.Item):
    # ztbRawInfo 表名称（文章信息存储表）
    subclass = scrapy.Field()  # 子类型
    site = scrapy.Field()  # 来源站点,域名
    page_url = scrapy.Field()  # 链接地址
    title = scrapy.Field()  # 标题
    issue_time = scrapy.Field()  # 发布时间
    creation_time = scrapy.Field()  # 抓取开始时间
    hubid = scrapy.Field()
    craw_status = scrapy.Field()
    craw_id = scrapy.Field()
    province_name = scrapy.Field()  # 省
    city_name = scrapy.Field()  # 市
    raw_data_id = scrapy.Field()  # 主表ID

    content = scrapy.Field()  # 主表ID

    download_url = scrapy.Field()
    file_name = scrapy.Field()
    attchments = scrapy.Field()
    tag_key =scrapy.Field()
    tag_value =scrapy.Field()

    ztb_ztbInfoType_tenderType = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='招标方类型')
    ztb_ztbInfoType_infoType = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='公告类型')
    ztb_ztbInfoType_sourceType = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='发标方类型')
    ztb_ztbInfo_qualification = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='资质要求')
    ztb_ztbInfo_registerMoney = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='注册资金')
    ztb_ztbInfo_resultsAmount = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='业绩金额')
    ztb_ztbInfo_buyTenderStartTime = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='购买标书时间')
    ztb_ztbInfo_buyTenderEndTime = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='购买标书截止时间')
    ztb_ztbInfo_bidDate = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='投标时间')
    ztb_ztbInfo_network = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='网络类型')
    ztb_project_tenderer = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='招标方')
    ztb_project_agent = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='代理方')
    ztb_project_candidate = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='中标候选人')
    ztb_ztbInfo_qualification_raw = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='资质要求: 原始数据')
    ztb_project_period_raw = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目周期原始数据')
    ztb_project_startTime_raw = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目的开始与结束时间原始数据')
    ztb_project_PersonInChargeRequirement = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目负责人要求')
    ztb_project_ProjectTeamRequirements = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目团队要求')
    project_amount = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目金额')
    str1 = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='预留str字段1长度20')
    str2 = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='预留str字段2长度20')
    int1 = scrapy.Field()  # Column(mysql.INTEGER(display_width=1), comment='预留int字段1长度1')
    int2 = scrapy.Field()  # Column(mysql.INTEGER(display_width=1), comment='预留int字段2长度1')
    json1 = scrapy.Field()  # Column(mysql.LONGTEXT, comment='存储json')
    create_time = scrapy.Field()  # Column(mysql.TIMESTAMP, )
    update_time = scrapy.Field()  # Column(mysql.TIMESTAMP, )
    business_type = scrapy.Field()  # Column(mysql.VARCHAR(length=255), comment='业务类型')
    purchase_type = scrapy.Field()  # Column(mysql.VARCHAR(length=255), comment='采购类型')



class ShangqingHubItem(scrapy.Item):
    # ztbRawInfo 表名称（文章信息存储表）
    subclass = scrapy.Field()  # 子类型
    site = scrapy.Field()  # 来源站点,域名
    page_url = scrapy.Field()  # 链接地址
    title = scrapy.Field()  # 标题
    issue_time = scrapy.Field()  # 发布时间
    creation_time = scrapy.Field()  # 抓取开始时间
    hubid = scrapy.Field()
    craw_status = scrapy.Field()
    craw_id = scrapy.Field()
    province_name = scrapy.Field()  # 省
    city_name = scrapy.Field()  # 市
    raw_data_id = scrapy.Field()  # 主表ID

    download_url = scrapy.Field()
    file_name = scrapy.Field()
    attchments = scrapy.Field()
    tag_key =scrapy.Field()
    tag_value =scrapy.Field()

    ztb_ztbInfoType_tenderType = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='招标方类型')
    ztb_ztbInfoType_infoType = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='公告类型')
    ztb_ztbInfoType_sourceType = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='发标方类型')
    ztb_ztbInfo_qualification = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='资质要求')
    ztb_ztbInfo_registerMoney = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='注册资金')
    ztb_ztbInfo_resultsAmount = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='业绩金额')
    ztb_ztbInfo_buyTenderStartTime = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='购买标书时间')
    ztb_ztbInfo_buyTenderEndTime = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='购买标书截止时间')
    ztb_ztbInfo_bidDate = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='投标时间')
    ztb_ztbInfo_network = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='网络类型')
    ztb_project_tenderer = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='招标方')
    ztb_project_agent = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='代理方')
    ztb_project_candidate = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='中标候选人')
    ztb_ztbInfo_qualification_raw = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='资质要求: 原始数据')
    ztb_project_period_raw = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目周期原始数据')
    ztb_project_startTime_raw = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目的开始与结束时间原始数据')
    ztb_project_PersonInChargeRequirement = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目负责人要求')
    ztb_project_ProjectTeamRequirements = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目团队要求')
    project_amount = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目金额')
    str1 = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='预留str字段1长度20')
    str2 = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='预留str字段2长度20')
    int1 = scrapy.Field()  # Column(mysql.INTEGER(display_width=1), comment='预留int字段1长度1')
    int2 = scrapy.Field()  # Column(mysql.INTEGER(display_width=1), comment='预留int字段2长度1')
    json1 = scrapy.Field()  # Column(mysql.LONGTEXT, comment='存储json')
    create_time = scrapy.Field()  # Column(mysql.TIMESTAMP, )
    update_time = scrapy.Field()  # Column(mysql.TIMESTAMP, )
    business_type = scrapy.Field()  # Column(mysql.VARCHAR(length=255), comment='业务类型')
    purchase_type = scrapy.Field()  # Column(mysql.VARCHAR(length=255), comment='采购类型')


class ShangqingArticleItem(scrapy.Item):
    # ztbRawInfo 表名称（文章信息存储表）
    subclass = scrapy.Field()  # 子类型
    site = scrapy.Field()  # 来源站点,域名
    page_url = scrapy.Field()  # 链接地址
    title = scrapy.Field()  # 标题
    issue_time = scrapy.Field()  # 发布时间
    creation_time = scrapy.Field()  # 抓取开始时间
    hubid = scrapy.Field()
    craw_status = scrapy.Field()
    craw_id = scrapy.Field()
    province_name = scrapy.Field()  # 省
    city_name = scrapy.Field()  # 市
    raw_data_id = scrapy.Field()  # 主表ID
    content = scrapy.Field()

    download_url = scrapy.Field()
    file_name = scrapy.Field()
    attchments = scrapy.Field()
    tag_key =scrapy.Field()
    tag_value =scrapy.Field()

    ztb_ztbInfoType_tenderType = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='招标方类型')
    ztb_ztbInfoType_infoType = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='公告类型')
    ztb_ztbInfoType_sourceType = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='发标方类型')
    ztb_ztbInfo_qualification = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='资质要求')
    ztb_ztbInfo_registerMoney = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='注册资金')
    ztb_ztbInfo_resultsAmount = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='业绩金额')
    ztb_ztbInfo_buyTenderStartTime = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='购买标书时间')
    ztb_ztbInfo_buyTenderEndTime = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='购买标书截止时间')
    ztb_ztbInfo_bidDate = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='投标时间')
    ztb_ztbInfo_network = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='网络类型')
    ztb_project_tenderer = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='招标方')
    ztb_project_agent = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='代理方')
    ztb_project_candidate = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='中标候选人')
    ztb_ztbInfo_qualification_raw = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='资质要求: 原始数据')
    ztb_project_period_raw = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目周期原始数据')
    ztb_project_startTime_raw = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目的开始与结束时间原始数据')
    ztb_project_PersonInChargeRequirement = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目负责人要求')
    ztb_project_ProjectTeamRequirements = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目团队要求')
    project_amount = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='项目金额')
    str1 = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='预留str字段1长度20')
    str2 = scrapy.Field()  # Column(mysql.VARCHAR(length=20), comment='预留str字段2长度20')
    int1 = scrapy.Field()  # Column(mysql.INTEGER(display_width=1), comment='预留int字段1长度1')
    int2 = scrapy.Field()  # Column(mysql.INTEGER(display_width=1), comment='预留int字段2长度1')
    json1 = scrapy.Field()  # Column(mysql.LONGTEXT, comment='存储json')
    create_time = scrapy.Field()  # Column(mysql.TIMESTAMP, )
    update_time = scrapy.Field()  # Column(mysql.TIMESTAMP, )
    business_type = scrapy.Field()  # Column(mysql.VARCHAR(length=255), comment='业务类型')
    purchase_type = scrapy.Field()  # Column(mysql.VARCHAR(length=255), comment='采购类型')