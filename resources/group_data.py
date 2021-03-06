import os
import sys
sys.path.insert(0, os.getcwd())

from utilities.pre_processing import tokenize, remove_stop_words, stemming
from xml.etree import ElementTree as ET
import os
import json
import sys


DATA_PATH = '/home/renzi/Documents/Jstor_txt_data'
key_words = ['Method','Materials and methods']
word_list = ['Introduction', 'Results', 'Discussion']
abstract_words = ['Key words', 'Summary', 'Abstract', 'INTRODUCTION', 'Introduction']
country = ' '.join(sys.argv[1:])


def file2text(file):
    try:
        tree = ET.parse(file)
    except:
        return {'text': '',
                'format': 'error'}
    root = tree.getroot()
    texts = ''
    file_format = ''
    if root.tag == 'plain_text':
        for child in root:
            if child.text:
                texts += child.text
        file_format = 'text'
    elif root.tag == 'body':
        for child in root:
            if child.text:
                texts += child.text
        file_format = 'xml'
    else:
        file_format = 'other'

    return {'text': texts,
            'format': file_format}


def get_methods(input_text):
    text = ''
    for key_word in key_words:
        if key_word.upper() in input_text:
            text = input_text.split(key_word.upper())[1]
            for word in word_list:
                if word.upper() in text:
                    text = text.split(word.upper())[0]
        if key_word in input_text:
            text = input_text.split(key_word)[1]
            for word in word_list:
                if word in text:
                    text = text.split(word)[0]
        if text:
            return text
    return text


def get_paper_list(country):
    with open(os.path.join(os.getcwd(), 'metadata', 'metadata.json')) as f:
        data = json.load(f)
    papers = [k for k, v in data.items() if 'countries' in v and country in v['countries']]
    return papers


def get_paper_list_from_method_coo(country):
    #with open(os.path.join(os.getcwd(), 'metadata', 'countries_METHOD', 'method_countries.json')) as f:
    with open(os.path.join(os.getcwd(), 'metadata', 'countries_0706', 'countries.json')) as f:
        data = json.load(f)
    papers = [k for k, v in data.items() if country in v and v[country] > 2]
    return papers


def get_texts(country):
    #file_list = get_paper_list(country)

    #file_list = get_paper_list_from_method_coo(country)
    file_list = get_paper_list(country)
    texts = []
    num_files = 0
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            if file.split('.')[0] in file_list:
                num_files += 1
                if num_files % 500 == 0:
                    print(num_files)
                parsed_result = file2text(os.path.join(root, file))
                method_text = get_methods(parsed_result['text'])
                if not method_text:
                    #raise ValueError('Methods is empty')
                    print('empty Mehotds')
                token_text = stemming(remove_stop_words(tokenize(method_text)))
                texts.append(token_text)
    print(num_files)
    with open(os.path.join(os.getcwd(), 'text', 'method_{}.json'.format(country)), 'w') as f:
        json.dump(texts, f)


def get_word2vec_texts(country):
    file_list = get_paper_list(country)
    texts = []
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            if file.split('.')[0] in file_list:
                parsed_result = file2text(os.path.join(root, file))
                method_text = get_methods(parsed_result['text'])
                for sentence in method_text.split('.'):
                    token_text = stemming(remove_stop_words(tokenize(sentence)))
                    if token_text:
                        texts.append(token_text)
    path = os.path.join(os.getcwd(), 'word2vec_text', '{}.json'.format(country))
    with open(path, 'w') as f:
        json.dump(texts, f)





if __name__ == '__main__':
    print(country)
    #get_texts(country)
    get_word2vec_texts(country)
