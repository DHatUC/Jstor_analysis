from xml.etree import ElementTree as ET
from pre_processing import tokenize, remove_stop_words, stemming, remove_lf_words
import os
import json
import pycountry
import re
import collections


key_words = ['Method','Materials and methods']
word_list = ['Introduction', 'Results', 'Discussion']
abstract_words = ['Key words', 'Summary', 'Abstract', 'INTRODUCTION', 'Introduction']
stop_words = ['AND', 'Georgia']
NUM_START, NUM_STOP = 0, 200000
OUTPUT_FILE = 'countries_1.json'
FOLDERS = ['a', 'b']


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


def get_country(text):
    for word in abstract_words:
        if word in text:
            text = text.split(word)[0]
        if word.upper() in text:
            text = text.split(word.upper())[0]
    countries = list(pycountry.countries)
    author_countries = []
    for country in countries:
        if country.alpha_3 not in stop_words and country.name not in stop_words:
            if re.search(r', {}\b'.format(country.name), text) \
                    or re.search(r', {}\b'.format(country.name.upper()), text) \
                    or re.search(r', {}\b'.format(country.alpha_3), text) \
                    or re.search(r', The {}\b'.format(country.name), text):
                if country.name not in author_countries:
                    author_countries.append(country.name)
    return author_countries


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


def load_file(path):
    texts = []
    num_files = 0
    num_methods = 0
    num_abstract = 0
    paper_attributes = {}
    country_counter = []
    for folder in os.listdir(path):
        if folder[0] in FOLDERS:
            for file in os.listdir(os.path.join(path, folder)):
                num_files += 1
                if num_files <= NUM_START:
                    continue
                parsed_result = file2text(os.path.join(path, folder, file))
                method_text = get_methods(parsed_result['text'])
                if method_text:
                    token_text = stemming(remove_stop_words(tokenize(method_text)))
                    texts.append(token_text)
                    num_methods += 1
                    author_countries = get_country(parsed_result['text'][:1000])
                    if len(author_countries) > 1:
                        num_abstract += 1
                        paper_id = file.split('.')[0]
                        paper_attributes[paper_id] = {'countries': author_countries}
                        for c in author_countries:
                            if c in country_counter:
                                country_counter[c] += 1
                            else:
                                country_counter[c] = 1
                if num_files % 1000 == 0:
                    print(num_files, num_methods, num_abstract)
    with open(os.path.join(os.getcwd(), 'metadata', OUTPUT_FILE), 'w') as f:
        json.dump(paper_attributes, f)
    print(country_counter)
    print("finished extraction")
    print(num_files, num_methods, num_abstract)

    #with open(os.path.join(os.getcwd(), 'text', 'method_full.json'), 'w') as f:
    #    json.dump(texts, f)


if __name__ == '__main__':
    load_file('/home/renzi/Documents/Jstor_txt_data')

