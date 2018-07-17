from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import os
import sys

#avg_similarities = [0.1205, 0.0989, 0.1055, 0.1313, 0.1487, 0.1692, 0.1499, 0.139, 0.1285, 0.1587, 0.1241, 0.1315, 0.1853]
#largest_similarities = [247.54, 250.06, 256.5, 260.14, 257.56, 294.31, 309.64, 256.54, 253.29, 291.89, 245.53, 266.04, 270.31]
countries = ['United States', 'France', 'Australia', 'Spain', 'India', 'China', 'Brazil', 'Mexico', 'Argentina',
             'South Africa', 'Malaysia', 'Chile', 'Kenya', 'Ecuador']


def load_file(filename):
    with open(os.path.join(os.getcwd(), 'lda_results', filename)) as f:
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
    print(res)
    return res


def plot_barchart(country):
    centroid_similarities = load_file('centroid_similarities.txt')[country]
    max_similarities = load_file('maximum_similarities.txt')[country]
    print(centroid_similarities)
    print(max_similarities)
    fig, ax = plt.subplots()
    index = np.arange(len(centroid_similarities))
    bar_width = 0.35
    value1 = [float(centroid_similarities[c]) for c in countries if c in centroid_similarities]
    value2 = [float(max_similarities[c]) for c in countries if c in max_similarities]
    x = [item / max(value1) for item in value1]
    print(x)
    y = [item / max(value2) for item in value2]
    compared_countries = (c for c in countries if c != country)
    rects1 = ax.bar(index, x, bar_width, label='Centroid distance')
    reacs2 = ax.bar(index + bar_width, y, bar_width, label='Maximum distance')
    ax.set_title('Distances between {} and other countries'.format(country))
    ax.set_xlabel('Countries')
    ax.set_ylabel('Distance')
    ax.set_xticks(index + bar_width / 2)
    plt.xticks(fontsize=6, rotation=90)
    ax.set_xticklabels(compared_countries)
    ax.legend(fontsize=6)
    fig.tight_layout()
    #plt.show()
    #os.mkdir(os.path.join(os.getcwd(), 'lda_html', country))
    plt.savefig(os.path.join(os.getcwd(), 'lda_html', country, 'distance.png'), bbox_inches='tight', dpi=500)


if __name__ == '__main__':
    #country = ' '.join(sys.argv[1:])
    for country in countries:
        plot_barchart(country)