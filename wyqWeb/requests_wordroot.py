# -*- coding: utf-8 -*-

import requests,json,re,pprint
from bs4 import BeautifulSoup

import pandas as pd
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
import sqlalchemy
MYSQLINFO= {
    "HOST": "localhost",
    "DBNAME": "english",
    "USER": "root",
    "PASSWORD": "040304",
    "PORT":3306
}
conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
                                                                                               'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME=MYSQLINFO[
                                                                                               'DBNAME'])
mysqlcon = sqlalchemy.create_engine(conStr)

def allpage():
    urlbase = 'http://www.etymon.cn/yingyucizhui/list_2_{}.html'
    for num in range(1,17):
        yield urlbase.format(str(num))


def request_artcl(url):
    brow = requests.get(url=url)
    html = brow.text.encode(brow.encoding).decode('utf-8')
    soup = BeautifulSoup(html,'lxml')
    # description = soup.find('dd',attrs={'name':'description'})
    description = soup.find('dd',attrs={'class':'highlight'})
    reword = description.get_text().replace('\r','').replace('\t','').replace('同源词：','')
    llist = reword.split('1.',1)
    llist[1] = "1." + llist[1]

    chart1 = llist[0].split('\n')
    sumary = '\n'.join([i for i in chart1 if i])
    chart2 = llist[1].split('\n')
    contentword = '\n'.join([i for i in chart2 if i])

    return sumary,contentword


def insert_mysql(itmeList):
    df = pd.DataFrame(itmeList)
    df.to_sql(name='wordroots', con=mysqlcon, if_exists='append', index=False,chunksize=1000)

def splitword(word):
    queer = "@#$#@"
    word = word.replace("，",',').replace("（",'(').replace("）",')').replace("-",'').replace(';',',')
    word = word.replace('ple(t)','ple').replace('mem(or)','mem,memor').replace('prag = prag;pract','prag,pract').replace('varic','词根 varic- = to straddle 跨坐, 横跨, 跨越')
    word = word.replace('it(i)','it,i').replace('avi (av) = bird','avi,av,au = bird').replace('surg(e)','surge,surg')
    word = word.replace('词根chron time 时间','词根chron = time时间').replace('jus(t)','jus,just')
    word = word.replace('(a)esthet,(a)esthes','aesthet,aesthes,esthet,esthes').replace('前缀draw = 拉，牵引','词根draw = 拉，牵引')

    if '词根' not in word:
        word = '词根' + word
    if '=' not in word:
        word = word + "="


    comma_in_brackets_compile = re.compile("\((.*?)\).*=")
    comma_in_brackets = ''.join(re.findall(comma_in_brackets_compile,word))
    # print(comma_in_brackets,'----------71')
    if comma_in_brackets:
        comma_in_brackets_queer = comma_in_brackets.replace(',',queer)
        word = word.replace(comma_in_brackets,comma_in_brackets_queer)

    regx = ''.join(re.findall("词[根裉](.*)=",word))
    # print(regx,'----82')
    if not regx:
        return None
    # print(regx,'----82')
    if ',' in regx:
        char_1_list = [i.replace('-','').replace(' ','').strip() for i in regx.split(',')]
        # print(char_1_list,'----87')
    else:
        char_1_list = [regx.replace('-','').replace(' ','').strip()]
        # print(char_1_list,'-----90')

    for num,i in enumerate(char_1_list):
        regx_in = re.compile("\((.*?)\)")
        regx_out = re.compile("(\(.*?\))")
        regx_in_word = ''.join(re.findall(regx_in,i))
        regx_out_word = ''.join(re.findall(regx_out,i))
        # print(regx_in_word,'-----96')
        # print(regx_out_word,'-----97')
        if regx_in_word and regx_out_word:
            baseword = i.replace(regx_out_word, '')
            char_1_list[num] = baseword
            regx_in_list = regx_in_word.split(queer)
            # print(regx_in_list,'----102')
            def tempory(wordd,baseword):
                corrlateword = ['i', 'o', 'y', 'e']
                if wordd in corrlateword:
                    newWord = baseword + wordd
                else:
                    newWord = wordd
                return newWord

            if len(regx_in_list) > 1:
                for nn in regx_in_list:
                    newWord = tempory(nn,baseword)
                    char_1_list.append(newWord)
            else:
                newWord = tempory(regx_in_list[0],baseword)
                char_1_list.append(newWord)
    return char_1_list

def etymon_main():

    for url in allpage():
        brow = requests.get(url=url)
        html = brow.text.encode(brow.encoding).decode('utf-8')
        soup = BeautifulSoup(html,'lxml')
        souphref = soup.select("#dictionary > dl > dt > a")
        itemList = []

        for i in souphref:
            url = "http://www.etymon.cn" + i.get('href')
            if '43117' in url:
                continue
            title = i.get_text()
            try:
                wordlist = splitword(title)
                subclass = 1
                description, cotent = request_artcl(url)
                combword = ','.join(wordlist)
                for nword in wordlist:
                    ddict = {}
                    ddict['title'] = title
                    ddict['description'] =description
                    ddict['cotent'] =cotent
                    ddict['combword'] =combword
                    ddict['subclass'] = subclass
                    ddict['url'] = url
                    ddict['word'] = nword
                    ddict['len'] = len(nword)
                    itemList.append(ddict)
            except Exception as f:
                print('error----------',f)
                print(url)
                ddict = {}
                ddict['url'] = url
                ddict['title'] = title
                ddict['error'] = 1
                itemList.append(ddict)


        insert_mysql(itemList)


def test():
    wword = "zetta- [ZE tuh]"
    a = splitword(wword)

    print('********************************')
    print(wword)
    print(a)
    print('********************************')

    exit()

    a = request_artcl("http://www.etymon.cn/yingyucigen/1982.html")
    a,b = request_artcl('http://www.etymon.cn/yingyucigen/2510.html')
    print(a)
    print(b)


def from_mysql_getallword():
    exc = "SELECT id,word,combword FROM wordroots"
    a = mysqlcon.execute(exc)
    llist = []
    for i in a:
        ddict = {}
        ddict['id'] = i[0]
        ddict['word'] = i[1]
        ddict['combword'] =i[2]
        llist.append(ddict)
    return pd.DataFrame(llist)

def splitword_2(word):

    word = word.replace("，",',').replace("（",'(').replace("）",')').replace(';',',')
    word = word.replace('coun)','coun-)').replace('acoust(o)-','acoust-,acousto-').replace('adip(o)-','adipo-,adip-')
    word = word.replace('adren(o)','adren-,adreno-').replace('aer(o)-','aero-,aer-').replace('ique','-ique')
    word = word.replace('tetra','tetra-').replace('tetr','tetr-')
    word = word.replace('trans(tran,tran,tres,treas) ','trans-,tran-,tran-,tres-,treas-').replace('ento','ento-')
    word = word.replace('-ward(s)','-wards,-ward').replace('acar(o)-','acar-,acaro-')
    word = word.replace('acanth(o)-','acanth-,acantho-').replace('abdomin(o)-','abdomin-,abdomino-')
    print(word)

    alist = re.findall("[a-zA-Z]{1,10}-",word)
    blist = re.findall("-[a-zA-Z]{1,10}", word)
    if alist:
        return alist
    elif blist:
        return blist
    else:
        return None


if __name__ == '__main__':

    # # wword = '前缀 re-(red-,ren-,r-)的词源，意思和用法'
    # wword = '前缀 aden-,adeno- = A gland'
    #
    # print(splitword_2(wword))
    # exit()
    import ssl
    from lxml import etree


    for num,url in enumerate(allpage()):
        # if num >0:
        #     break
        brow = requests.get(url=url)
        html = brow.text.encode(brow.encoding).decode('utf-8')

        respon = etree.HTML(html)
        souphref = respon.xpath("/html/body/div[@id='container']/div[@id='dictionary']/dl/dt/a/@href")
        itemList = []

        for i in souphref:
            url = "http://www.etymon.cn" + i
            title = respon.xpath("//*[@href = '{}']/text()".format(i))[0]
            try:
                wordlist = splitword_2(title)
                subclass = 1
                # description, cotent = request_artcl(url)
                combword = ','.join(wordlist)
                for nword in wordlist:
                    ddict = {}
                    ddict['title'] = title
                    # ddict['description'] = description
                    # ddict['cotent'] = cotent
                    ddict['combword'] = combword
                    ddict['subclass'] = subclass
                    ddict['url'] = url
                    ddict['word'] = nword
                    ddict['len'] = len(nword)
                    pprint.pprint(ddict)
                    itemList.append(ddict)
            except Exception as f:
                print('error----------', f)
                print(url)
                ddict = {}
                ddict['url'] = url
                ddict['title'] = title
                ddict['error'] = 1
                itemList.append(ddict)



        # insert_mysql(itemList)


    pass


