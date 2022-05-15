import csv
import sys
#import pandas as pd
csvinput = sys.argv[1]
csvoutput = sys.argv[2]
num = int(sys.argv[3])
fout = open(csvoutput, 'w')
r = []
#with open(csvinput,encoding = 'utf-8') as text:
#    row = csv.reader(text, delimiter = '\t')
fin = open(csvinput, 'r')
lines = fin.readlines()
fin.close()
row = []
for line in lines:
    row.append(line.split('\t'))
if True:
    for r in row:
        if r[num] == 'None':
            fout.write(r[0] + '\n')
fout.close()
"""
    with open(csvoutput, 'wb') as csvout:
        #csvwriter = csv.writer(csvout, delimiter = '\t')
        for r in row:
            print(r)
            #csvwriter.writerow(r)
            csvout.write('\t'.join(r))
"""
