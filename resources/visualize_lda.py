from gensim import models
from gensim.corpora import Dictionary
import pyLDAvis.gensim
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import json
import sys
import argparse


#country = ' '.join(sys.argv[1:])
#version = '2nd'


def visualize_lda(path, country, version):
    def load_corpus():
        with open(os.path.join(path, 'text', 'method_{}.json'.format(country))) as f:
            texts = json.load(f)
        return [dictionary.doc2bow(text) for text in texts]

    lda_model = models.LdaModel.load(os.path.join(path, 'lda_results', country, version, 'lda_model'))
    dictionary = Dictionary.load(os.path.join(path, 'lda_results', country, version, 'dictionary'))
    print('a')
    corpus = load_corpus()
    print('b')
    vis_data = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    print('c')
    #pyLDAvis.display(vis_data)
    pyLDAvis.save_html(vis_data, os.path.join(path, 'lda_html', 'lda_{}{}.html'.format(country, 'method_coo_25t200p')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare distances between models')
    parser.add_argument('--country', help='Country name', nargs='+', required=True)
    parser.add_argument('--version', help='Version', default='')
    args = parser.parse_args()
    country1 = ' '.join(args.country)
    version1 = args.version
    visualize_lda(os.getcwd(), country1, version1)