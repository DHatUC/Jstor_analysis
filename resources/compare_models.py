from scipy.spatial.distance import cosine
from matplotlib import pyplot as plt
from gensim import models
import numpy as np
import os
import re
import random
import argparse


NUM_TOPICS = 15
NUM_WORDS = 100


def load_data(country, version=''):
    path = os.path.join(os.getcwd(), 'lda_results', country, version, 'lda_model')
    model = models.LdaModel.load(path)
    return model


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


class DistanceModel:

    def __init__(self, topic_model1, topic_model2):
        topic_list1 = topic_model1.get_topics()
        topic_list2 = topic_model2.get_topics()
        self.dictionary = set(topic_model1.get_dictionary()).intersection(topic_model2.get_dictionary())
        self.topics1 = [[topic[word] if word in topic else 0 for word in self.dictionary] for topic in topic_list1]
        self.topics2 = [[topic[word] if word in topic else 0 for word in self.dictionary] for topic in topic_list2]
        self.topic_words1 = [[word for word in topic] for topic in topic_list1]
        self.topic_words2 = [[word for word in topic] for topic in topic_list2]

    def calculate_topic_similarities(self, normalization=False):
        if normalization:
            topics1 = [[t / sum(topic) for t in topic]for topic in self.topics1]
            topics2 = [[t / sum(topic) for t in topic]for topic in self.topics2]
        else:
            topics1 = self.topics1
            topics2 = self.topics2
        similarities = []
        for idx1, topic1 in enumerate(topics1):
            for idx2, topic2 in enumerate(topics2):
                similarities.append(cosine(topic1, topic2))
        num_bins = np.arange(0.0, 0.5, 0.01)
        plt.hist(similarities, num_bins)
        print(len([x for x in similarities if x < 0.5]) / len(similarities))
        #plt.show()
        sorted_similarities = sorted(similarities)
        for i in range(50):
            idx = similarities.index(sorted_similarities[i])
            a = int((idx + 1) / 25)
            b = (idx + 1) % 25 - 1
            print(similarities[idx], '|', self.topic_words1[a][:10], '|',  self.topic_words2[b][:10])

    def find_best_match_cosine_similarity(self):
        matrix = {}
        for idx1, topic1 in enumerate(self.topics1):
            matrix[idx1] = []
            for idx2, topic2 in enumerate(self.topics2):
                matrix[idx1].append(cosine(topic1, topic2) + random.randint(0, 100) / 1000000)
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
        for idx, topic in enumerate(self.topic_words1):
            cos_distances.append(matrix[idx][hits[idx]['hit']])
            num_words = len([word for word in topic if word in self.topic_words2[hits[idx]['hit']]])
            overlapping_words.append(num_words)
        print(np.mean(cos_distances))
        print(len([x for x in cos_distances if x < 0.4]))
        print(np.mean(cos_distances), cos_distances)
        #print(overlapping_words)
        #print(np.mean(overlapping_words))

    def find_best_match_overlapping_words(self):
        matrix = {}
        for idx1, topic1 in enumerate(self.topic_words1):
            matrix[idx1] = []
            for idx2, topic2 in enumerate(self.topic_words2):
                matrix[idx1].append(len([x for x in topic1 if x in topic2]) / len(topic1) + random.randint(0, 100) / 1000000)
        hits = {}
        for idx, vectors in matrix.items():
            max_distance = sorted(vectors, reverse=True)[0]
            max_idx = vectors.index(max_distance)
            hits[idx] = {'hit': max_idx, 'rank': 0, 'distance': max_distance}
        has_new_change = True
        while has_new_change:
            has_new_change = False
            temp = []
            for idx, vector in hits.items():
                if vector['hit'] not in temp:
                    temp.append(vector['hit'])
                else:
                    idx_compared = [k for k, v in hits.items() if v['hit'] == vector['hit']][0]
                    if matrix[idx][vector['hit']] > matrix[idx_compared][vector['hit']]:
                        current_vector = hits[idx_compared]
                        updated_hit = matrix[idx_compared].index(sorted(matrix[idx_compared], reverse=True)[current_vector['rank'] + 1])
                        hits[idx_compared] = {'hit': updated_hit, 'rank': current_vector['rank'] + 1, 'distance': matrix[idx_compared][updated_hit]}
                    else:
                        current_vector = hits[idx]
                        updated_hit = matrix[idx]. index(sorted(matrix[idx], reverse=True)[current_vector['rank'] + 1])
                        hits[idx] = {'hit': updated_hit, 'rank': current_vector['rank'] + 1, 'distance': matrix[idx_compared][updated_hit]}
                    has_new_change = True
        overlapping_words = []
        for idx, topic in enumerate(self.topic_words1):
            num_words = len([word for word in topic if word in self.topic_words2[hits[idx]['hit']]])
            overlapping_words.append(num_words)
        print(overlapping_words)
        print(np.mean(overlapping_words))


def main():
    parser = argparse.ArgumentParser(description='Compare distances between models')
    parser.add_argument('--c1', help='Country name 1', nargs='+', required=True)
    parser.add_argument('--c2', help='Country name 2', nargs='+', required=True)
    parser.add_argument('--v1', help='Version 1', default='')
    parser.add_argument('--v2', help='Version 2', default='')
    args = parser.parse_args()
    country1, country2 = ' '.join(args.c1), ' '.join(args.c2)
    version1, version2 = args.v1, args.v2

    model1 = load_data(country1, version=version1)
    model2 = load_data(country2, version=version2)
    topic_model1 = TopicModel(model1)
    topic_model2 = TopicModel(model2)
    print(country1)
    distance_model = DistanceModel(topic_model1, topic_model2)
    #distance_model.calculate_topic_similarities(normalization=True)
    distance_model.find_best_match_cosine_similarity()
    #distance_model.find_best_match_overlapping_words()


if __name__ == '__main__':
    main()
