from gensim import models
from scipy.spatial.distance import cosine
import numpy as np
import os
import re
import random
import sys

NUM_TOPICS = 25
NUM_WORDS = 100
NUM_TOPICS_MATCH = 20
COUNTRY = sys.argv[1]
VERSION = '25t200p'


class TopicModel:
    def __init__(self, model):
        self.topics = []
        self.dictionary = []
        topic_list = model.print_topics(num_topics=NUM_TOPICS, num_words=NUM_WORDS)
        pattern = r'0.\d{3}\*"\w+"'
        for topic in topic_list:
            topic_string = re.findall(pattern, topic[1])
            topic = {}
            for w in topic_string:
                topic[w.split('"')[1]] = float(w.split('*')[0])
            self.topics.append(topic)

            for w in topic_string:
                word = w.split('"')[1]
                if word not in self.dictionary:
                    self.dictionary.append(word)

    def get_topics(self):
        return self.topics

    def get_dictionary(self):
        return self.dictionary


def cosine_distance(topics1, topics2, dictionary1, dictionary2):
    dictionary = list(set(dictionary1 + dictionary2))
    padding_topics1 = [[topic[word] if word in topic else 0 for word in dictionary] for topic in topics1]
    padding_topics2 = [[topic[word] if word in topic else 0 for word in dictionary] for topic in topics2]
    matrix = {}
    for idx1, topic1 in enumerate(padding_topics1):
        matrix[idx1] = []
        for idx2, topic2 in enumerate(padding_topics2):
            matrix[idx1].append(cosine(topic1, topic2) + random.randint(0, 100) / 1000000)
            #matrix[idx1].append(cosine(topic1, topic2))
    hits = {}
    for idx, vectors in matrix.items():
        min_distance = sorted(vectors)[0]
        min_idx = vectors.index(min_distance)
        hits[idx] = {'hit': min_idx, 'rank': 0, 'distance': min_distance}
    has_new_change = True
    while has_new_change:
        has_new_change = False
        temp = []
        for idx, vector in hits.items():
            if vector['hit'] not in temp:
                temp.append(vector['hit'])
            else:
                idx_compared = [k for k, v in hits.items() if v['hit'] == vector['hit']][0]
                if matrix[idx][vector['hit']] < matrix[idx_compared][vector['hit']]:
                    current_vector = hits[idx_compared]
                    updated_hit = matrix[idx_compared].index(sorted(matrix[idx_compared])[current_vector['rank'] + 1])
                    hits[idx_compared] = {'hit': updated_hit, 'rank': current_vector['rank'] + 1, 'distance': matrix[idx_compared][updated_hit]}
                else:
                    current_vector = hits[idx]
                    updated_hit = matrix[idx]. index(sorted(matrix[idx])[current_vector['rank'] + 1])
                    hits[idx] = {'hit': updated_hit, 'rank': current_vector['rank'] + 1, 'distance': matrix[idx_compared][updated_hit]}
                has_new_change = True

    cos_distances = []
    overlapping_words = []
    for idx, topic in enumerate(topics1):
        cos_distances.append(matrix[idx][hits[idx]['hit']])
        num_words = len([word for word in topic if word in topics2[hits[idx]['hit']]])
        overlapping_words.append(num_words)
    top_cos_distances = sorted(cos_distances)[0: NUM_TOPICS_MATCH]
    #return np.mean(cos_distances)
    return np.mean(top_cos_distances)
    #return NUM_WORDS - len([x for x in cos_distances if x < 0.4])
    #return 1 - len([x for x in cos_distances if x < 0.4])


class ModelSet:
    def __init__(self, country, version):
        self.models = {}
        path = os.path.join(os.getcwd(), 'lda_results')
        for folder in os.listdir(os.path.join(path, country)):
            if folder.startswith(version):
                model = models.LdaModel.load(os.path.join(path, country, folder, 'lda_model'))
                self.models[folder] = TopicModel(model)

    def get_representative_model(self):
        avg_distances = {}
        for idx1, model1 in self.models.items():
            avg_distances[idx1] = 0
            for idx2, model2 in self.models.items():
                if idx1 != idx2:
                    avg_distances[idx1] += cosine_distance(model1.get_topics(), model2.get_topics(),
                                                           model1.get_dictionary(), model2.get_dictionary())
            avg_distances[idx1] = avg_distances[idx1] / 4
        print(avg_distances)
        ###print(max(avg_distances.iteritems(), key=operator.itemgetter(1))[0])
        print(min(avg_distances, key=avg_distances.get))


def main():
    print(COUNTRY)
    model_set = ModelSet(COUNTRY, VERSION)
    model_set.get_representative_model()


if __name__ == '__main__':
    main()


