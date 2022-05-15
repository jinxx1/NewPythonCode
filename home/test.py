import pprint
import re, pprint

count = 100
a_pro = 0.99
b_pro = 0.95

no_a_count = count - (count * a_pro)
_pre = 1 - b_pro
print(no_a_count/_pre)
