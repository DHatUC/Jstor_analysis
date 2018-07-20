from scipy.spatial.distance import cosine
from matplotlib import pyplot as plt
from gensim import models
import numpy as np
import os
import re


NUM_TOPICS = 25
NUM_WORDS = 0

def load_data(country):
    path = os.path.join(os.getcwd(), 'lda_results', country, 'lda_model')
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
        dct = {}
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
            print(similarities[idx], '|', self.topic_words1[a][:10],'|',  self.topic_words2[b][:10])


def main():
    country1, country2 = 'United States', 'Mexico'
    model1 = load_data(country1)
    model2 = load_data(country2)
    topic_model1 = TopicModel(model1)
    topic_model2 = TopicModel(model2)
    distance_model = DistanceModel(topic_model1, topic_model2)
    distance_model.calculate_topic_similarities(normalization=True)


if __name__ == '__main__':
    main()
