import re
f=open("Ӣ���ı�.txt") 
#��ȡ�ļ��е��ַ���
txt = f.read()
 #ȥ���ַ����еı�㡢���ֵ�
txt = re.sub('[,\.()":;!@#$%^&*\d+-/?"<>]|\'s|\'', '', txt)
#�滻���з�����Сдת������ֳɵ����б�
word_list = txt.replace('\n',' ').replace('  ',' ').lower().split(' ')
d = {}#����һ�����ֵ�
for word in word_list:
#ͳ���ֵ��еĴ�Ƶ
    if word in d.keys():
        d[word] += 1
    else:
        d[word] =1
#���յ��ʳ��ִ�������
d= sorted(d.items(), key=lambda x:x[1], reverse=True)
#������ļ�
f1=open("��Ƶͳ��.txt", 'w')
for i in d:
    f1.write("%s\t%s\n" %(i[0],str(i[1])))
f1.close()


