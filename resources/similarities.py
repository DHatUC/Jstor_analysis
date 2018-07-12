from gensim import models
import re
import os
import sys

NUM_TOPICS = 25
NUM_WORDS = 20

COUNTRY1 = 'China'
COUNTRY2 = 'Kenya'


def load_data(country):
    path = os.path.join(os.getcwd(), 'lda_results', country, 'lda_model')
    model = models.LdaModel.load(path)
    return model


def vector_similarity(d1, d2):
        v1_words = [k for k, v in d1.items()]
        v2_words = [k for k, v in d2.items()]
        words = set(v1_words).intersection(v2_words)
        similarity = 0
        for word in words:
            if word in d1 and d2:
                similarity += abs(d1[word] - d2[word])
            elif word in d1:
                similarity += abs(d1[word])
            elif word in d2:
                similarity += abs(d2[word])
        return similarity / len(words)


class Dictionary:
    def __init__(self):
        self.words = []

    def add_model(self, model):
        topic_list = model.print_topics(num_topics=NUM_TOPICS, NUM_WORDS=NUM_WORDS)
        pattern = r'0.\d{3}\*"\w+"'
        for topic in topic_list:
            topic_strings = re.findall(pattern, topic[1])
            words = [word.split('"')[1] for word in topic_strings]
            for word in words:
                if word not in self.words:
                    self.words.append(word)

    def word_list(self):
        return self.words


class TopicModel:
    def __init__(self, model):
        self.topics = []
        self.dictionary =[]
        self.center = {}
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

        for word in self.dictionary:
            s = 0
            for topic in self.topics:
                if word in topic:
                    s += topic[word]
            self.center[word] = s / len(self.topics)

    def get_topics(self):
        return self.topics

    def get_dictionary(self):
        return self.dictionary

    def get_center(self):
        return self.center

    def inner_topic_similarity(self):
        s = 0
        #for idx1, t1 in enumerate(self.topics):
        #    for idx2, t2 in enumerate(self.topics):
        #        if idx1 < idx2:
        #            s += vector_similarity(t1, t2)
        #return s / ((len(self.topics) * len(self.topics) - 1) / 2)
        for topic in self.topics:
            s += vector_similarity(self.center, topic)
        return s / len(self.topics)


class DistanceModel:
    def __init__(self, topic_model1, topic_model2):
        self.topics1 = topic_model1.get_topics()
        self.topics2 = topic_model2.get_topics()
        self.dictionary = set(topic_model1.get_dictionary()).intersection(topic_model2.get_dictionary())

    def inter_model_similarity(self):
        s = 0
        for t1 in self.topics1:
            for t2 in self.topics2:
                s += vector_similarity(t1, t2)
        similarity = s / len(self.topics1) / len(self.topics2)
        return similarity


def main(country1, country2):
    model1 = load_data(country1)
    model2 = load_data(country2)
    topic_model1 = TopicModel(model1)
    topic_model2 = TopicModel(model2)
    inner_s_1 = topic_model1.inner_topic_similarity()
    inner_s_2 = topic_model2.inner_topic_similarity()
    inter = vector_similarity(topic_model1.get_center(), topic_model2.get_center())
    return inter * inter / inner_s_1 / inner_s_2


if __name__ == '__main__':
    main(COUNTRY1, COUNTRY2)
    countries = ['United States', 'France', 'Australia', 'Spain', 'India', 'China', 'Brazil', 'Mexico', 'Argentina',
                 'South Africa', 'Malaysia', 'Chile', 'Kenya', 'Ecuador']
    f = open(os.path.join(os.getcwd(), 'lda_results', 'similarities.txt'), 'w')
    for idx1, value1 in enumerate(countries):
        for idx2, value2 in enumerate(countries):
            if idx1 < idx2:
                f.write(str(main(value1, value2))[0:6])
            f.write('\t')
        f.write('\n')
    f.close()



