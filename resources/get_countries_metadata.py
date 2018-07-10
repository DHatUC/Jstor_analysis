from xml.etree import ElementTree as ET
from pre_processing.pre_processing import tokenize, remove_stop_words, stemming, remove_lf_words
import os
import json
import pycountry
import re
import collections


key_words = ['Method','Materials and methods']
word_list = ['Introduction', 'Results', 'Discussion']
abstract_words = ['Key words', 'Summary', 'Abstract', 'INTRODUCTION', 'Introduction']
states_USA = ['AL', 'AK', 'AZ', 'AR', 'AA', 'AE', 'AP', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL',
              'IN','IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
              'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA',
              'WV', 'WI', 'WY']
stop_words = ['AND', 'Georgia']
NUM_START, NUM_STOP = 0, 200000
OUTPUT_FILE = 'countries_os.json'
FOLDERS = ['o', 'p', 'q', 'r', 's']


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
    for state in states_USA:
        if re.search(r', {}'.format(state), text):
            if 'United States' not in author_countries:
                author_countries.append('United States')
    return author_countries


def get_methods(input_text):
    for key_word in key_words:
        if key_word.upper() in input_text:
            text = input_text.split(key_word.upper())[1]
            for word in word_list:
                if word.upper() in text:
                    return True
        if key_word in input_text:
            text = input_text.split(key_word)[1]
            for word in word_list:
                if word in text:
                    return True
    return False


def load_file(path):
    num_files = 0
    num_methods = 0
    num_abstract = 0
    paper_attributes = {}
    country_counter = {}
    for folder in os.listdir(path):
        if folder[0] in FOLDERS:
            print(folder)
            for file in os.listdir(os.path.join(path, folder)):
                num_files += 1
                parsed_result = file2text(os.path.join(path, folder, file))
                method_text = get_methods(parsed_result['text'])
                if method_text:
                    num_methods += 1
                    author_countries = get_country(parsed_result['text'][:1000])
                    if len(author_countries) > 0:
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


if __name__ == '__main__':
    load_file('/home/renzi/Documents/Jstor_txt_data')