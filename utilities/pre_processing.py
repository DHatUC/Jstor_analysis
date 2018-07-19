from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
import os
import collections
import json
import math
import re


def tokenize(text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text.lower())
    return tokens


def remove_stop_words(text):

    shakespare_stops = ['thou', 'thee', 'thy', 'thine', 'ye', 'shall', 'will', 'lord', 'sir', 'good', 'love', 'now', 'come', 'king']
    stops = get_stop_words('en')
    tokens = [x for x in text if x and x not in stops and x not in shakespare_stops and len(x) > 2]
    return tokens


def stemming(text):

    porter_stemmer = PorterStemmer()
    tokens = [porter_stemmer.stem(x) for x in text]
    return tokens


def remove_low_frequent_words(text, min_count):
    path = os.path.join(os.getcwd(), 'data', 'word_count.json')
    with open(path) as f:
        word_count = json.load(f)
    res = [w for w in text if word_count[w] >= min_count]
    return res


def get_tfidf_collections():
    path = os.path.join(os.getcwd(), 'data\Folger_txt')
    words = []
    docs = []
    for file_name in os.listdir(path):
        with open(os.path.join(path, file_name)) as f:
            text = f.read()
        doc_list = re.split(r'Scene [0-9]{1,2}', text)
        for doc in doc_list:
            if len(doc) > 100:
                doc = stemming(tokenize(doc))
                docs.append(doc)
        text = tokenize(text)
        text = stemming(text)
        for word in text:
            if word not in words:
                words.append(word)
    print(len(docs))
    idfs = {}
    for word in words:
        count = 0
        for doc in docs:
            if word in doc:
                count += 1
        idfs[word] = math.log(len(docs) / (count + 1))
    with open(os.path.join(os.getcwd(), 'data\word_idf.json'), 'w') as f:
        json.dump(idfs, f, indent=4)


def get_tfidf_words(doc, cutoff):
    if not os.path.isfile(os.path.join(os.getcwd(), 'data\word_idf.json')):
        print('Building word frequency library')
        get_tfidf_collections()
    with open(os.path.join(os.getcwd(), 'data\word_idf.json')) as f:
        idfs = json.load(f)
    words = collections.Counter(doc)
    max_f = max([words[x] for x in words])
    res = []
    tfidf_dict = {}
    for word in words:
        tf = 0.5 + 0.5 * words[word] / max_f
        idf = idfs[word]
        if tf * idf > cutoff:
            res.append(word)
    #    tfidf_dict[word] = tf * idf
    #with open(os.path.join(os.getcwd(), 'data\word_tfidf.json'), 'w') as f:
    #    json.dump(tfidf_dict, f, indent=2)
    return res


def remove_lf_words(text, min_count):
    word_counter = collections.Counter(text)
    return [word for word, count in word_counter.items() if count >= min_count]