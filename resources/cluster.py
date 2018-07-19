from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import os

countries = ['United States', 'France', 'Australia', 'Spain', 'India', 'China', 'Brazil', 'Mexico', 'Argentina',
             'South Africa', 'Malaysia', 'Chile', 'Kenya', 'Ecuador']

PATH = os.path.join(os.getcwd(), 'lda_results', 'maximum_similarities.txt')


def load_file(path):
    with open(path) as f:
        data = f.read()
    res = {}
    idx = -1
    for line in data.split('\n'):
        if len(line) > 0:
            idx += 1
            temp = {}
            values = [x for x in line.split('\t') if len(x) > 0]
            for i in range(len(values)):
                temp[countries[len(countries) - len(values) + i]] = values[i]
            res[countries[idx]] = temp

    for country in countries:
        for key, item in res.items():
            if country != key and country not in item:
                item[country] = res[country][key]
    return res


class GroupClassifier:
    def __init__(self, similarities):
        self.groups = {i: [countries[i]] for i in range(len(countries))}
        self.linkage = []
        self.idx = len(countries)
        self.similarities = similarities

    def merge_groups(self, idx1, idx2, distance):
        group = self.groups[idx1] + self.groups[idx2]
        self.groups[self.idx] = group
        self.idx += 1
        del self.groups[idx1]
        del self.groups[idx2]
        self.linkage.append([idx1, idx2, distance, len(group)])

    def find_min_distance(self):
        min_distance = 10000000
        res = [0, 0]
        for idx1, values1 in self.groups.items():
            for idx2, values2 in self.groups.items():
                if idx1 < idx2:
                    for value1 in values1:
                        for value2 in values2:
                            if float(self.similarities[value1][value2]) < min_distance:
                                res = [idx1, idx2]
                                min_distance = float(self.similarities[value1][value2])
        return res, min_distance

    def find_max_distance(self):
        min_distance = 10000000000
        res = [0, 0]
        for idx1, values1 in self.groups.items():
            for idx2, values2 in self.groups.items():
                if idx1 < idx2:
                    max_group_distance, temp_idx = 0, 0
                    for value1 in values1:
                        for value2 in values2:
                            if float(self.similarities[value1][value2]) > max_group_distance:
                                max_group_distance = float(self.similarities[value1][value2])
                    if max_group_distance < min_distance:
                        res = [idx1, idx2]
                        min_distance = max_group_distance
        return res, min_distance

    def run(self, linkage='single'):
        while len(self.groups) > 1:
            if linkage == 'single':
                [idx1, idx2], distance = self.find_min_distance()
            elif linkage == 'complete':
                [idx1, idx2], distance = self.find_max_distance()
            else:
                raise ValueError()
            self.merge_groups(idx1, idx2, distance)
        return self.linkage


def main():
    similarities = load_file(PATH)
    classifier = GroupClassifier(similarities)
    linkage = classifier.run()
    dendrogram(linkage, labels=countries, leaf_font_size=4, leaf_rotation=90, color_threshold=0)
    plt.savefig(os.path.join(os.getcwd(), 'dendrogram.png'), dpi=500)
    #plt.show()


if __name__ == '__main__':
    main()

