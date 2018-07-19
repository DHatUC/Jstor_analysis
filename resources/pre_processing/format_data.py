from xml.etree import ElementTree as ET
from utilities.pre_processing import tokenize, remove_stop_words, stemming, remove_lf_words
import os
import json


word_list = ['Introduction', 'Methods', 'Results', 'Discussion']


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


def explore_structure(text):
    for word in word_list:
        if word in text or word.upper() in text or word.lower() in text:
            return True


def tokenize_text(text):
    token_text = stemming(remove_stop_words(tokenize(text)))
    filetered_text = remove_lf_words(token_text, 2)
    return filetered_text


def load_file(path, output_file_path):
    texts = []
    num_txt = 0
    num_xml = 0
    format_counter = {'text': 0,
                      'xml': 0,
                      'error': 0,
                      'other': 0}
    k = 0
    num_structure = 0
    print(len(os.listdir(path)))
    for file in os.listdir(path):
        k += 1
        parsed_result = file2text(os.path.join(path, file))
        texts.append(tokenize_text(parsed_result['text']))
        format_counter[parsed_result['format']] += 1
        if parsed_result['format'] == 'text':
            num_txt += 1
        else:
            num_xml += 1
        if k % 1000 == 0:
            print(k, format_counter)

        if explore_structure(parsed_result['text']):
            num_structure += 1

    print(format_counter)
    print(num_structure)
    with open(output_file_path, 'w') as f:
        json.dump(texts, f)


if __name__ == '__main__':
    #file2text(os.path.join(os.getcwd(), 'data', '110990.txt'))
    #file2text(os.path.join(os.getcwd(), 'data', '380571.txt'))
    data_path = os.path.join(os.getcwd(), 'data')
    output_path = os.path.join(os.getcwd(), 'text', 'small_sample.txt')
    load_file(data_path, output_path)