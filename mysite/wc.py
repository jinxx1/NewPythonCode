from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
from collections import Counter
# jieba.load_userdict("txt\userdict.txt")
# 添加用户词库为主词典,原词典变为非主词典
from wordcloud import WordCloud, ImageColorGenerator

# 获取当前文件路径
# __file__ 为当前文件, 在ide中运行此行会报错,可改为
# d = path.dirname('.')
#d = path.dirname(__file__)

stopwords = {}
isCN = 1 #默认启用中文分词
#back_coloring_path = "img/background.jpg" # 设置背景图片路径
font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc' # 为matplotlib设置中>文字体路径没
stopwords_path = 'stopwords1893.txt' # 停用词词表
imgname1 = "WordCloudDefautColors.png" # 保存的图片名字1(只按照背景图片形状)
imgname2 = "WordCloudColorsByImg.png"# 保存的图片名字2(颜色按照背景图片颜色布局>生成)

#back_coloring = imread(path.join(d, back_coloring_path))# 设置背景图片

# 设置词云属性
wc = WordCloud(font_path=font_path,  # 设置字体
               background_color="white",  # 背景颜色
               max_words=2000,  # 词云显示的最大词数
               mask=None,  # 设置背景图片
               max_font_size=100,  # 字体最大值
               random_state=42,
               width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使>用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
               )

def jiebaclearText(text):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr="/ ".join(seg_list)
    f_stop = open(stopwords_path)
    try:
        f_stop_text = f_stop.read( )
        #f_stop_text=unicode(f_stop_text,'utf-8')
    finally:
        f_stop.close( )
    f_stop_seg_list=f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
            mywordlist.append(myword)
    c = Counter()
    for x in mywordlist:
        if len(x)>1 and x != '\r\n' and x != '\n':
            c[x] += 1
    text_common = ""
    for (k,v) in c.most_common(100):
        text_common += k + "\t" + str(v) + "\n"

    tcfile = open("wordslist.txt", 'w')
    tcfile.write(text_common)
    tcfile.close()
    return ''.join(mywordlist)

def wc_generate(text,d,imgname):
    text = jiebaclearText(text)

    # 生成词云, 可以用generate输入全部文本(wordcloud对中文分词支持不好,建议启用中文>分词),也可以我们计算好词频后使用generate_from_frequencies函数
    wc.generate(text)

    # 保存图片
    wc.to_file(path.join(d, imgname))

if __name__ == "__main__":
    d = '/home/terry'
    fname = "text.png"
    wc_generate("生成词云, 可以用generate输入全部文本(wordcloud对中文分词支持不好,建议启用中文>分词),也可以我们计算好词频后使用generate_from_frequencies函数",d,fname)
