import sys
import os
sys.path.insert(0, os.getcwd())
from utilities.timer import Timer

from gensim import corpora, models
import json

NUM_TOPICS = 25
PASSES = 200
version = '200pass_2'

country = ' '.join(sys.argv[1:])


def prepare_dict(path):
    with open(os.path.join(path, 'text', 'method_{}.json'.format(country))) as f:
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
    ldamodel = models.LdaMulticore(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=PASSES, workers=4)
    t3.ends()
    os.mkdir(os.path.join(path, 'lda_results', country, version))
    ldamodel.save(os.path.join(path, 'lda_results', country, version, 'lda_model'))
    dictionary.save(os.path.join(path, 'lda_results', country, version, 'dictionary'))


if __name__ == '__main__':
    load_file(os.getcwd())