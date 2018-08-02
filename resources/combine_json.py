import json
import os


def merge_json(path, name):
    res = {}
    for file in os.listdir(path):
        if file.startswith(name):
            print(file)
            with open(os.path.join(path, file)) as f:
                dct = json.load(f)
                print(len(dct))
                for key, value in dct.items():
                    res[key] = value
    with open(os.path.join(path, '{}.json'.format(name)), 'w') as f:
        json.dump(res, f)
        print(len(res))


if __name__ == '__main__':
    #merge_json(os.path.join(os.getcwd(), 'metadata'), 'year_journal')
    #merge_json((os.path.join(os.getcwd(), 'metadata')), 'countries')
    merge_json(os.path.join(os.getcwd(), 'metadata', 'countries_METHOD'), 'method_countries')