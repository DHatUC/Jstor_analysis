from matplotlib import pyplot as plt
import json
import os
import collections
import sys

COUNTRY_CUTTOFF = int(sys.argv[1])


def filter_data(data, cutoff=1):
    filtered_data = {}
    for key, countries in data.items():
        temp = {}
        for country, count in countries.items():
            if count >= cutoff:
                temp[country] = count
        if temp:
            filtered_data[key] = temp
    return filtered_data


def hist_countries():
    with open(os.path.join(os.getcwd(), 'metadata', 'countries_METHOD', 'method_countries.json')) as f:
        data = json.load(f)

    filtered_data = filter_data(data, cutoff=COUNTRY_CUTTOFF)

    num_countries = []
    num_country_all = []
    for key, countries in filtered_data.items():
        num_countries.append(len(countries))
        num_country_all.append(sum([int(v) for k, v in countries.items()]))
    #fig, axs = plt.subplots(1, 2, sharey= True, tight_layout=True)
    print('Num of countries', collections.Counter(num_countries))
    print()
    print('Num of presence', collections.Counter(num_country_all))

    n_bins = range(20)
    #axs[0].hist(num_countries, bins=n_bins)
    #axs[1].hist(num_country_all, bins=n_bins)
    #axs[0].set_title('Histogram of number of countries')
    #axs[1].set_title('Histogram of number of country name presence')
    plt.hist(num_countries, bins=n_bins)
    plt.title('Histogram of documents by number of countries', fontsize=6)
    plt.savefig(os.path.join(os.getcwd(), 'metadata', 'Histogram of documents by number of method CoO'))
    #plt.show()


def statistics_countries():
    with open(os.path.join(os.getcwd(), 'metadata', 'countries_METHOD', 'method_countries.json')) as f:
        method_countries = json.load(f)
    with open(os.path.join(os.getcwd(), 'metadata', 'countries_0706', 'countries.json')) as f:
        author_countries = json.load(f)

    filtered_data = filter_data(method_countries, cutoff=COUNTRY_CUTTOFF)
    num_same = 0
    num_author_countries = 0
    num = 0
    hist_match = {}
    num_1_1, num_1_2, num_2_1, num_2_2 = 0, 0 , 0, 0
    for j_id, countries in filtered_data.items():
        if j_id not in author_countries:
            print(j_id)
            continue
        num_match = 0
        if 'countries' in author_countries[j_id]:
            num_author_countries += 1
            for country in countries:
                if country in author_countries[j_id]['countries']:
                    num_match += 1
        if num_match > 0:
            num_same += 1
            if num_match not in hist_match:
                hist_match[num_match] = 1
            else:
                hist_match[num_match] += 1
            if num_match == 1:
                if len(author_countries[j_id]['countries']) == 1:
                    num_1_1 += 1
                else:
                    num_2_1 += 1
            else:
                if len(author_countries[j_id]['countries']) == 1:
                    num_1_2 += 1
                else:
                    num_2_2 += 1
        num += 1
    print(num_same)
    print(num_author_countries)
    print(num)
    print(hist_match)
    print(num_1_1, num_1_2, num_2_1, num_2_2)
    labels = ['Authors from one country studied in same country',
              'Authors from multiple countries studied in one of their countries',
              'Authors from multiple countries studied in multiple countries',
              'Studies in different countries of authors']
    sizes = [num_1_1, num_2_1, num_2_2, num - num_same]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    #explode = (0.1, 0, 0, 0)  # explode 1st slice
    #patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    patches, texts, sth = plt.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=False, startangle=140)
    plt.legend(patches, labels, loc="best", fontsize=6)
    plt.axis('equal')
    #plt.tight_layout()
    #plt.show()
    plt.savefig(os.path.join(os.getcwd(), 'metadata', 'methods_countries.png'), dpi=700)


def main():
    #statistics_countries()
    hist_countries()


if __name__ == '__main__':
    main()


