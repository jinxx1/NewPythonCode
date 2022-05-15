import os,pymysql


SECRET_KEY = 'you-guess'

ROOT = 'http://120.79.192.168:6800/'
# ROOT = 'http://localhost:6800/'



# 个人站点配置信息
# 站点标题
SITE_TITLE = 'u学在线门户网站'
# 站点副标题
SITE_SUBTITLE = 'u学在线门户网站—副标题。'

# 放置 md 文件夹
# 文章 md 文件夹
POST_PATH = './source/_posts/'
POST_BAK_PATH = './source/_postsBak/'

INSERT_PIC = './quiet/static/insertPic/'
# 页面 md 文件夹
PAGE_PATH = './source/_pages/'
PAGE_BAK_PATH = './source/_pagesBak/'
# 输出 html 文件夹
GENERATED_PATH = './quiet/static/generated/'
# 默认分类
DEFAULT_CATEGORY = '未分类'
# 默认标签
DEFAULT_TAG = ['其他']

# 存放 shelve 数据文件
BLOG_DAT = './quiet/static/generated/data'

# 管理员信息,建议配置环境变量
# 登录名，密码
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME') or 'jinxiao'
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD') or '1'

# mysql数据库
DB_MYSQL = pymysql.connect(
    host="120.24.4.84",
    db="jubang",
    user="xey",
    passwd="85f0a9e2e63b47c0b56202824195fb70#AAA",
    charset="utf8",
    use_unicode=True,
    cursorclass=pymysql.cursors.DictCursor
)
# DB_MYSQL = pymysql.connect(
#     host="localhost",
#     db="jubang",
#     user="root",
#     passwd="040304",
#     charset="utf8",
#     use_unicode=True,
#     cursorclass=pymysql.cursors.DictCursor
# )
# COOKIE手工选用
COOKIES_DATA = '''BIDUPSID=DD88D030347178141A41E498E6001A79; PSTM=1547441019; BDUSS=GZTVEtCVlZsaWgyVjdnRzczTDFmem5PVzlkVDNGQXNxQjhkSkx3aH4wRmNVNGhjQVFBQUFBJCQAAAAAAAAAAAEAAAAQk54AamlueHgxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFzGYFxcxmBca; BAIDUID=DD88D030347178141A41E498E6001A79:SL=0:NR=50:FG=1; bdindexid=oc7a118p8s5utrngdpscgrnu17; CHKFORREG=27e617490b66f111cd1b271fbb511d2d; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=2; ZD_ENTRY=google; H_PS_PSSID=1469_21083_28608_28585_28557_28518_28606; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1551708977,1551767140; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1551767145

'''


