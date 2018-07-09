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
                res.update(dct)
    with open(os.path.join(path, '{}.json'.format(name)), 'w') as f:
        json.dump(res, f)
        print(len(res))


if __name__ == '__main__':
    #merge_json(os.path.join(os.getcwd(), 'metadata'), 'year_journal')
    merge_json((os.path.join(os.getcwd(), 'meta', 'metadata')), 'countries')