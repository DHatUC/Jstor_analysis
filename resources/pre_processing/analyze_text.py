from timer import Timer
from xml.etree import ElementTree as ET
from utilities.pre_processing import tokenize, remove_stop_words, stemming, remove_lf_words
import os
import json


word_list = ['Introduction', 'Methods', 'Results', 'Discussion']


def explore_text(text):
    count = 0
    #for word in word_list:
    #    if word.upper() in text:# or word.lower() in text:
    #        count += 1
    if 'METHODS' in text or 'Methods' in text:
        count += 1
    return count


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


def analyze_text(path):
    count_dict = {i: 0 for i in range(5)}
    for file in os.listdir(path):
        parsed_result = file2text(os.path.join(path, file))
        count_dict[explore_text(parsed_result['text'])] += 1
    print(count_dict)


if __name__ == '__main__':
    timer = Timer('Text analysis')
    analyze_text(os.path.join(os.getcwd(), 'data'))
    timer.ends()
