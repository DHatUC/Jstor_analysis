from gensim import models
from gensim.corpora import Dictionary
import pyLDAvis.gensim
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import json
import sys


country = ' '.join(sys.argv[1:])
version = '2nd'


def visualize_lda(path):
    lda_model = models.LdaModel.load(os.path.join(path, 'lda_results', country, version, 'lda_model'))
    dictionary = Dictionary.load(os.path.join(path, 'lda_results', country, version, 'dictionary'))
    with open(os.path.join(path, 'text', 'method_{}.json'.format(country))) as f:
        texts = json.load(f)
    corpus = [dictionary.doc2bow(text) for text in texts]
    vis_data = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    pyLDAvis.display(vis_data)
    pyLDAvis.save_html(vis_data, os.path.join(path, 'lda_html', 'lda_{}{}.html'.format(country, version)))


if __name__ == '__main__':
    visualize_lda(os.getcwd())