# -*- coding: utf-8 -*-
text_path = r'C:\Users\jinxx\Downloads\Documents\XDF词根词缀记忆大全.pdf'
# -*- coding: utf-8 -*-
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator



def Pdf2Txt(Path,Save_name):
    #来创建一个pdf文档分析器
    parser = PDFParser(Path)
    #创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr=PDFResourceManager()
        # 设定参数进行分析
        laparams=LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device=PDFPageAggregator(rsrcmgr,laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter=PDFPageInterpreter(rsrcmgr,device)
        # 处理每一页
        for Num,page in enumerate(PDFPage.create_pages(document)):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout=device.get_result()
            print('---------------------------', Num)
            for num,x in enumerate(layout):
                pass

                if (isinstance(x, LTTextBoxHorizontal)):
                    print(x.get_text().encode('utf-8').decode('utf-8'))
                    with open(Save_name.format(str(Num)),'a') as f:
                        f.write(x.get_text()+'\n')



if __name__ == '__main__':
    Path = open(text_path, 'rb')
    Pdf2Txt(Path,'engexam/b{}.txt')