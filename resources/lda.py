import sys
import os
sys.path.insert(0, os.getcwd())
from utilities.timer import Timer

from gensim import corpora, models
import json
import argparse

NUM_TOPICS = 25
PASSES = 200
parser = argparse.ArgumentParser(description='Run LDA on a country and generate a new version')
parser.add_argument('--country', help='Country name', nargs='+', required=True)
parser.add_argument('--version', type=str, default='', help='A version name')
args = parser.parse_args()
country = ' '.join(args.country)
version = args.version


def prepare_dict(path):
    with open(os.path.join(path, 'text', 'method_coo', 'method_{}.json'.format(country))) as f:
        texts = json.load(f)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    return dictionary, corpus


def load_file(path):
    t1 = Timer("Load text")
    dictionary, corpus = prepare_dict(path)
    t1.ends()
    t3 = Timer("LDA")
    #ldamodel = models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=PASSES)
    ldamodel = models.LdaMulticore(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=PASSES, workers=2)
    t3.ends()
    country_dir = os.path.join(path, 'lda_results', country, 'method_coo')
    if not os.path.isdir(country_dir):
        os.mkdir(country_dir)
    version_dir = os.path.join(country_dir, version)
    if not os.path.isdir(version_dir):
        os.mkdir(version_dir)
    ldamodel.save(os.path.join(path, 'lda_results', country, 'method_coo', version, 'lda_model'))
    dictionary.save(os.path.join(path, 'lda_results', country, 'method_coo', version, 'dictionary'))


if __name__ == '__main__':
    load_file(os.getcwd())