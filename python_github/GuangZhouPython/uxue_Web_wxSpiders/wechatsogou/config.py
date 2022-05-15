# -*- coding: utf-8 -*-

# 缓存配置
cache_dir = 'cache'
cache_session_name = 'requests_wechatsogou_session'

# mysql数据库配置
host = 'localhost'
# user = 'xey'   # 数据库用户名 root
# passwd = '85f0a9e2e63b47c0b56202824195fb70#AAA'   # 数据库密码040304
user = 'root'   # 数据库用户名 root
passwd = '040304'   # 数据库密码040304
db = 'jubang'  # 默认数据库
charset = 'utf8mb4'
prefix = ''  # 默认数据表前缀,可以不用写

# 打码平台配置ruokuai  http://www.ruokuai.com/
# 注册并充值后，就可以直接使用，识别一个验证码大约0.008元
# 搜狗微信有点变态，有时明明验证码是正确的，他非说是错误的，这是没有办法的事情,好在这个概率非常低
dama_name = 'jinxx1'    #用户名
dama_pswd = 'aa040304'  #密码
