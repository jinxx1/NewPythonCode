from flask import Blueprint, jsonify
from flask import render_template,flash,redirect,url_for
from utils import ImportData


api = Blueprint('api', __name__)


@api.route('/posts',methods=["POST","GET"])
def get_posts():
    """
    所有文章信息
    :return: json
    """
    a = ImportData.get_data().get('post_data')
    retuneList = []
    for d1 in a:
        # 处理预览图地址
        articlImgCUT = d1['articlePreviewImg'].split('static')[1]
        d1['articlePreviewImg'] = '/static' + articlImgCUT
        # 处理作者头像地址
        articlImgCUT = d1['authorImg'].split('static')[1]
        d1['authorImg'] = '/static' + articlImgCUT
        # 处理url
        urlT = ''
        if 'post/' not in d1['url']:
            timeGS = d1['datetime'].split('-')
            urlT = '/post/' + timeGS[0] + "/" + timeGS[1] + "/" + d1['url']
            d1['url'] = urlT

        retuneList.append(d1)

    return jsonify(retuneList)


@api.route('/post/<int:id>',methods=["POST","GET"])
def get_post(id):
    """
    指定 id 文章信息
    """
    for p in ImportData.get_data().get('post_data'):
        if p.get('id') == id:

            return jsonify(p)
    return jsonify({'msg': '没有数据'})


@api.route('/pages',methods=["POST","GET"])
def get_pages():
    """
    所有页面
    """

    return jsonify(ImportData.get_data().get('page_data'))


@api.route('/page/<url>',methods=["POST","GET"])
def get_page(url):
    """
    指定页面信息
    """
    for p in ImportData.get_data().get('page_data'):
        if p.get('url') == url:

            return jsonify(p)
    return jsonify({'msg': '没有数据'})


@api.route('/tags',methods=["POST","GET"])
def get_tags():
    """
    所有标签信息
    """

    return jsonify(ImportData.get_data().get('tag_data'))


@api.route('/tag/<tag>',methods=["POST","GET"])
def get_tag(tag):
    """
    指定标签信息
    """
    for t in ImportData.get_data().get('tag_data'):
        if t.get('tag') == tag:

            return jsonify(t)
    return jsonify({'msg': '没有数据'})


@api.route('/categories',methods=["POST","GET"])
def get_categories():
    """
    所有分类信息
    """

    return jsonify(ImportData.get_data().get('category_data'))


@api.route('/category/<cate>',methods=["POST","GET"])
def get_category(cate):
    """
    指定分类信息
    """
    for c in ImportData.get_data().get('category_data'):
        if c.get('category') == cate:

            return jsonify(c)
    return jsonify({'msg': '没有数据'})


@api.route('/newsLetterList',methods=["POST","GET"])
def newsLetterList():
    """
    首页快讯
    """
    listDict = []
    for c in ImportData.get_data().get('post_data'):
        city = '北京'
        dict = {
        'datetime':c['datetime'],
        'city':city,
        'title':c['title'],
        'summary':c['summary'],
        'url':c['url']

        }
        listDict.append(dict)


    return jsonify(listDict)


@api.route('/hotArticles',methods=["POST","GET"])
def hotArticles():
    """
    作者热门文章
    """
    listDict = []
    i = 0
    for c in ImportData.get_data().get('post_data'):
        if i > 4:
            break
        listDict.append(c)
        i+=1
    return jsonify(listDict)


@api.route('/recommendPosts',methods=["POST","GET"])
def recommendPosts():
    """
    推荐文章
    """
    listDict = []
    i = 0
    for c in ImportData.get_data().get('post_data'):
        if i > 4:
            break
        listDict.append(c)
        i+=1
    return jsonify(listDict)




