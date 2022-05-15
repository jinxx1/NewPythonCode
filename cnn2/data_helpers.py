import numpy as np
import re
import os
import jieba
import itertools
from collections import Counter
import words

jieba.load_userdict('dict.txt')
#classes = ['0','1','2','3','4','5','6','7','8','9','10']
label_list_11 = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]
#classes_num = len(labelnames.label_names)

def get_label_name(id):
    import labelnames
    return labelnames.label_names[id]

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

padding_word = "<PAD/>"

def load_texts(datalist,max_sequence_length,vocabulary):
    ret = []
    for data in datalist:
        data = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、：“”~@#￥%……&*（）]+", "", data)
        sentence = list(jieba.cut(data))
        #print(sentence)
        new_sentence = []
        for item in sentence:
            if item in words.keywords:
                continue
            new_sentence.append(item)
        #new_sentence = sentence
        num_padding = max_sequence_length - len(new_sentence)
        if num_padding > 0:
            new_sentence = new_sentence + [padding_word] * num_padding
        keywords = []
        for word in new_sentence:
            if len(keywords) >= max_sequence_length:
                continue
            try:
                keywords.append(vocabulary[word])
            except Exception as e:
                print(e)
                keywords.append(0)
                pass
        #item = np.array(keywords)
        ret.append(np.array(keywords))
    return np.array(ret)
 
def load_text(data,max_sequence_length):
    sentence = list(jieba.cut(data))
    num_padding = max_sequence_length - len(sentence)
    new_sentence = sentence + [padding_word] * num_padding
    x, y, vocabulary, vocabulary_inv = load_data()
    print(vocabulary)
    ret = np.array([vocabulary[word] for word in new_sentence])
    return ret

def load_data(data_path,classes_num):
    sentences, labels = load_data_label(data_path,classes_num)
    sentences_padded = pad_sentences(sentences)
    vocabulary, vocabulary_inv = build_vocab(sentences_padded)
    x, y = build_input_data(sentences_padded, labels, vocabulary)
    return [x, y, vocabulary, vocabulary_inv]


def build_vocab(sentences):
    word_counts = Counter(itertools.chain(*sentences))
    vocabulary_inv = [x[0] for x in word_counts.most_common()]
    vocabulary = {x: i for i, x in enumerate(vocabulary_inv)}
    return [vocabulary, vocabulary_inv]


def pad_sentences(sentences):
    sequence_length = max(len(x) for x in sentences)
    padded_sentences = []
    for i in range(len(sentences)):
        sentence = sentences[i]
        num_padding = sequence_length - len(sentence)
        new_sentence = sentence + [padding_word] * num_padding
        padded_sentences.append(new_sentence)
    return padded_sentences


def build_input_data(sentences, labels, vocabulary):
    x = np.array([[vocabulary[word] for word in sentence] for sentence in sentences])
    y = np.array(labels)
    return [x, y]


def load_data_label(base_path,classes_num):
    print("loading data and label from :%s" % base_path)
    post_list = []
    label_list = []
    labels = []
    for j in range(classes_num):
        label = []
        for jj in range(j):
            label.append(0)
        label.append(1)
        for jj in range(classes_num - j - 1):
            label.append(0)
        labels.append(label)
    print(labels)
    i = 0
    for c in range(classes_num):
        c = str(c)
        print("loading " + c)
        file_list = os.listdir(base_path + c)
        for files in file_list:
            f = open(base_path + c + '/' + files, 'r', encoding='utf8', errors='ignore')
            temp = f.read().replace('nbsp', '')
            data = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、：“”~@#￥%……&*（）]+", "", temp)
            # data = ''.join(re.findall(u'[\u4e00-\u9fff]+', text))
            _data = list(jieba.cut(data))
            __data = []
            for item in _data:
                if item in words.keywords:
                    continue
                __data.append(item)
            post_list.append(__data)
            label_list.append(labels[i])
            f.close()
        i += 1
    return post_list, label_list

def load_data_label_n(path):
    post_list = []
    all_words = []
    label_list = []
    labels = label_list_11
    #labels = [0,1,2,3,4,5,6,7,8,9,10]
    i = 0
    for c in classes:
        file_list = os.listdir(path + c)
        for files in file_list:
            f = open(path + c + '/' + files, 'r', encoding='utf8', errors='ignore')
            temp = f.read().replace('nbsp', '')
            data = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、：“”~@#￥%……&*（）]+", "", temp)
            # data = ''.join(re.findall(u'[\u4e00-\u9fff]+', text))
            #_data = list(jieba.cut(data))
            post_list.append(data)
            """
            for item in _data:
                if item in words.keywords:
                    continue
                all_words.append(item)
            """
            label_list.append(labels[i])
            f.close()
        i += 1
    print(len(post_list), len(label_list))
    return [post_list, np.array(list(label_list))]


def load_data_and_labels(positive_data_file, negative_data_file):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    positive_examples = list(open(positive_data_file, "r", encoding='utf-8').readlines())
    positive_examples = [s.strip() for s in positive_examples]
    negative_examples = list(open(negative_data_file, "r", encoding='utf-8').readlines())
    negative_examples = [s.strip() for s in negative_examples]
    # Split by words
    x_text = positive_examples + negative_examples
    x_text = [clean_str(sent) for sent in x_text]
    # Generate labels
    positive_labels = [[0, 1] for _ in positive_examples]
    negative_labels = [[1, 0] for _ in negative_examples]
    y = np.concatenate([positive_labels, negative_labels], 0)
    return [x_text, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]
