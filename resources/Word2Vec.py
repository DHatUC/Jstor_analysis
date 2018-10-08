import gensim
from gensim.models import Word2Vec
from gensim.models import word2vec
import logging
import re
from nltk.corpus import stopwords
from nltk import sent_tokenize, word_tokenize
from gensim.models import Word2Vec
import logging
import nltk.data
import os
import json
nltk.download('stopwords')
nltk.download('punkt')
tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')


# These are parameters that can be tweaked to accomodate the corpus

num_features = 100    # Word vector dimensionalty
min_word_count = 3afd   # Minimum word count (ie. Only count words that show at least the min times)
num_workers = 4       # Number of threads to run in parallel
context = 10          # Context window size (ie. how many words surrounding the target word will count towards)                                                                                  
downsampling = 1e-3


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    path = os.path.join(os.getcwd(), 'word2vec_text', 'United States.json')
    with open(path) as f:
        data = json.load(f)
    model = gensim.models.Word2Vec(data, workers=num_workers, size=num_features, min_count = min_word_count, window = context, sample = downsampling)
    path = os.path.join(os.getcwd(), 'word2vec_model', 'United States_model')
    model.save(path) #save the model for future use or analysis
    #load model
    # model = Word2Vec.load('model name')

    print(model) #to see model vocab size
    print(model.wv.vocab) #display model vocab

    #model.most_similar(positive='', topn=30) #view the words that have the highest correlation to the target word
    #model.most_similar(positive='', negative='') #view words that are related to the (positive) but not related to the (negative)


if __name__ == '__main__':
    main()