import time
import datetime
import json
from ast import literal_eval

import nltk,re
from nltk.corpus import brown

# nltk.download('averaged_perceptron_tagger')
# nltk.download()

word = 'advertisement'

print(re.findall("[a-zA-Z](ment)[a-zA-Z]",word))