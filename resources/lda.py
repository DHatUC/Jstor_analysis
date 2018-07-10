from gensim import corpora, models
from pre_processing.timer import Timer
import sys

import json
import os

NUM_TOPICS = 25
PASSES = 100

country = sys.argv[1]


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
    os.mkdir(os.path.join(path, 'lda_results', country))
    ldamodel.save(os.path.join(path, 'lda_results', country, 'lda_model'))
    dictionary.save(os.path.join(path, 'lda_results', country, 'dictionary'))


if __name__ == '__main__':
    load_file(os.getcwd())