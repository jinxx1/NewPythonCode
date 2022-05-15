from flask import Blueprint, jsonify
from flask import render_template,flash,redirect,url_for
# from utils import ImportData
import pprint,os,shutil,shelve
# from config import BLOG_DAT
import requests
# a = ImportData.get_data()['post_data']
# print(a)
# filenameList = []
# for filename in a:
#     aa = filename['filename']
#     print(aa)
#     pprint.pprint(filename)
#     print('-------------------------------------')
#
# _data = {}
# data = shelve.open(BLOG_DAT, writeback=True)
# # pprint.pprint(iata.keys())
# for nn in data.keys():
#     print(nn)
# for n in data['post_data']:
#     print(n)
# for i in data['category_data']:
#     print(i)

# XXhtml = [fn['filename'] for fn in data['post_data']]
# if '23.html' not in XXhtml:
#     print('ok')
# else:
#     print('no')
# for i in data['post_data']:
#
#     pprint.pprint(i['filename'])
#
#     print('-------------------------------------')
# # data.close()

# data = shelve.open(BLOG_DAT, writeback=True)
# for i in data:
#     cls._data[i] = data[i]
# data.close()

#
# folder = r"E:\python_github\GuangZhouPython\uxue_Web\source\_posts"
# BakFolder = r'E:\python_github\GuangZhouPython\uxue_Web\source\_postsBak'
# for root, dirs, files in os.walk(BakFolder):
#     print('-------------------------------start')
#     print(root)
#     print(dirs)
#     print(files)
#     print(os.walk(BakFolder))
#     print('------------------------------end')
#     for name in files:
#         print(name)
#         print(os.path.splitext(name))
#         if os.path.splitext(name)[1].lower() == '.md':
#             md = os.path.join(root, name)
#             print(md)



            # Bak_Md_File_Path = shutil.move(md,BakFolder)
            # print(Bak_Md_File_Path)
import json
url = 'http://120.79.192.168:6800/api/posts'
# url = 'http://localhost:6800/api/posts'
# url = 'http://120.79.192.168:6800/api/tags'
# url = 'http://120.79.192.168:6800/api/pages'
# url = 'http://120.79.192.168:6800/api/categories'
# url = 'http://120.79.192.168:6800/api/pages'
# url = 'http://120.79.192.168:6800/api/newsLetterList'
# url = 'http://120.79.192.168:6800/api/hotArticles'
# url = 'http://localhost:6800/api/recommendPosts'
#
post1 = requests.get(url=url).text
a = json.loads(post1)
# IMPORT = ImportData.get_data().get('category_data')
n = 1
for i in a:
    pprint.pprint(i)
    n+=1
    print('--------{}---------'.format(n))
# pprint.pprint(a[])
# pprint.pprint(post1)
# from markdown import Markdown
#
# word1 = '''title: 数说未来第一篇文章
# summary: 第5篇文章
# url: 5555_5555
# datetime: 2019-02-28
# category: 数说未来
# articlePreviewImg: http://120.79.192.168:6800/static/img/pc/articleImg.png
# authorImg: http://120.79.192.168:6800/static/img/pc/userAvatar.png
# tag: 未来
#      数字
#
#
# ##555 Hello world555
# '''
#
# md = Markdown(extensions=['meta'])
# html = md.convert(word1)
#
# print(html.get['authorimg'][0])


# pprint.pprint(ImportData.get_data().get('post_data'))
# a = ImportData.get_data().get('post_data')
# retuneList = []
# for d1 in a:
#     #处理预览图地址
#     articlImgCUT = d1['articlePreviewImg'].split('quiet')[1]
#     d1['articlePreviewImg'] = articlImgCUT
#     # 处理作者头像地址
#     articlImgCUT = d1['authorImg'].split('quiet')[1]
#     d1['authorImg'] = articlImgCUT
#     # 处理url
#     timeGS = d1['datetime'].split('-')
#     urlT = 'post/' + timeGS[0] + "/" + timeGS[1] + "/" + d1['url']
#     d1['url'] =urlT
#     retuneList.append(d1)
#
#
# pprint.pprint(retuneList)

# import re
# a = '黑'
# a = 'hei'
# zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
#
# word = a.encode('utf-8').decode('utf-8')
# match = zh_pattern.search(word)
# print(match)
#
# if match:
#     print(True)
# else:
#     print(False)

