
import os
import json

PATH_YEAR_JOURNAL = os.path.join(os.getcwd(), 'metadata', 'year_journal.json')
PATH_COUNTRIES = os.path.join(os.getcwd(), 'metadata', 'countries.json')
PATH_OUTPUT = os.path.join(os.getcwd(), 'metadata', 'metadata.json')


def load_file():
    with open(PATH_YEAR_JOURNAL) as f:
        dct_year = json.load(f)
    with open(PATH_COUNTRIES) as f:
        dct_countries = json.load(f)

    res = dct_year.copy()
    for paper_id in dct_year:
        if paper_id in dct_countries:
            res[paper_id]['countries'] = dct_countries[paper_id]['countries']

    with open(PATH_OUTPUT, 'w') as f:
        json.dump(res, f)


if __name__ == '__main__':
    load_file()

