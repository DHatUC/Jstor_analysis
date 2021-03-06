from xml.etree import ElementTree as ET
import os
import json
import pycountry
import re
import collections
import argparse
from operator import itemgetter


key_words = ['Method','Materials and methods']
word_list = ['Introduction', 'Results', 'Discussion']
abstract_words = ['Key words', 'Summary', 'Abstract', 'INTRODUCTION', 'Introduction']
states_USA_abbreviation = ['AL', 'AK', 'AZ', 'AR', 'AA', 'AE', 'AP', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI',
                           'ID', 'IL', 'IN','IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
                           'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD',
                           'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
states_USA = ['Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
              'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
              'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
              'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
              'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
              'Tennessee', 'Texas', 'Utah', 'Vermont','Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
stop_words = ['AND', 'Georgia']
parser = argparse.ArgumentParser('Detect countries in documents')
parser.add_argument('folders', metavar='N',  nargs='+', help='Initials of journals')
args = parser.parse_args()
FOLDERS = args.folders
OUTPUT_FILE = 'countries_{}{}.json'.format(FOLDERS[0], FOLDERS[-1])
REGION_COUNT_CUTOFF = 3


def file2text(file):
    try:
        tree = ET.parse(file)
    except:
        return {'text': '',
                'format': 'error'}
    root = tree.getroot()
    texts = ''
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
    for state in states_USA_abbreviation:
        if re.search(r', {}'.format(state), text):
            if 'United States' not in author_countries:
                author_countries.append('United States')
    return author_countries


def get_countries_from_method(text):
    countries = list(pycountry.countries)
    author_countries = {}
    for country in countries:
        if country.alpha_3 not in stop_words and country.name not in stop_words:
            search_result_len = len(re.findall(r'{}\b'.format(country.name), text)) \
                                + len(re.findall(r'{}\b'.format(country.name.upper()), text)) \
                                + len(re.findall(r'The {}\b'.format(country.name), text))
            if search_result_len > 0:
                if country.name not in author_countries:
                    author_countries[country.name] = search_result_len
                else:
                    author_countries[country.name] += search_result_len
    for state in states_USA:
        search_result = re.findall(r'{}\b'.format(state), text)
        if len(search_result) > 0:
            if 'United States' in author_countries:
                author_countries['United States'] += len(search_result)
            else:
                author_countries['United States'] = len(search_result)
    for state_ab in states_USA_abbreviation:
        search_result = re.findall(r', {}\b'.format(state_ab), text)
        if len(search_result) > 0:
            if 'United States' in author_countries:
                author_countries['United States'] += len(search_result)
            else:
                author_countries['United States'] = len(search_result)
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


def get_method_coo_new_list(input_text):
    region_file_path = os.path.join(os.getcwd(), 'temp', 'country_region.json')
    with open(region_file_path) as f:
        regions = json.load(f)
    region_record = {}
    countries = []
    for region, country in regions.items():
        frequency = len(re.findall(r'{}\b'.format(region), input_text))
        if frequency >= REGION_COUNT_CUTOFF:
            countries.append(country)
            region_record[region] = frequency
    return countries, region_record


def load_file(path):
    num_files = 0
    num_methods = 0
    num_abstract = 0
    paper_attributes = {}
    country_counter = {}
    method_countries_dict = {}
    regions = {}
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
                        paper_id = file.split('.txt')[0]
                        paper_attributes[paper_id] = {'countries': author_countries}
                        method_countries = get_countries_from_method(method_text)
                        if method_countries:
                            method_countries_dict[paper_id] = {'old_method_coo': method_countries}
                        for c in author_countries:
                            if c in country_counter:
                                country_counter[c] += 1
                            else:
                                country_counter[c] = 1

                        countries, regions_frequency = get_method_coo_new_list(method_text)
                        if len(countries) > 0:
                            method_countries_dict[paper_id] = {'new_method_coo': countries}
                            for region, frequency in regions_frequency.items():
                                if region not in regions:
                                    regions[region] = frequency
                                else:
                                    regions[region] += frequency

                if num_files % 1000 == 0:
                    print(num_files, num_methods, num_abstract)
    filename = os.path.join(os.getcwd(), 'metadata', 'countries_METHOD', 'method_countries_{}.json'.format(FOLDERS[0] + FOLDERS[-1]))
    with open(filename, 'w') as f:
        json.dump(method_countries_dict, f)
    #with open(os.path.join(os.getcwd(), 'metadata', OUTPUT_FILE), 'w') as f:
    #    json.dump(paper_attributes, f)

    sorted_regions = sorted(regions.items(), key=itemgetter(1), reverse=True)
    with open(os.path.join(os.getcwd(), 'metadata', 'region_frequency_{}.json'.format(FOLDERS[0] + FOLDERS[-1])), 'w') as f:
        json.dump(sorted_regions, f)
    #print(country_counter)
    print("finished extraction")
    print(num_files, num_methods, num_abstract)


if __name__ == '__main__':
    load_file('/home/renzi/Documents/Jstor_txt_data')