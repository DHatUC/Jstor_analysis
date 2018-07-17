import matplotlib.pyplot as plt
import numpy as np
import json
import operator
import os
import collections

PATH_METADATA = os.path.join(os.getcwd(), 'metadata', 'metadata.json')


class Metadata:
    def __init__(self, path):
        with open(path) as f:
            self.data = json.load(f)

    def year_histogram(self):
        years = [int(v['year']) for k, v in self.data.items()]
        plt.hist(years)
        plt.show()

    def compare_on_year(self):
        year_with_countries = [int(v['year']) for k, v in self.data.items() if 'countries' in v]
        year_wo_countries = [int(v['year']) for k, v in self.data.items() if 'countries' not in v]
        print('Average year for papers with countries: ', np.mean(year_with_countries))
        print('Average year for papers without countries: ', np.mean(year_wo_countries))
        n_bins = range(1660, 2040, 10)
        fig, axs = plt.subplots(1, 2, sharey= True, tight_layout=True)

        SMALL_SIZE = 8
        MEDIUM_SIZE = 10
        BIGGER_SIZE = 12

        plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


        axs[0].hist(year_with_countries, bins=n_bins)
        axs[1].hist(year_wo_countries, bins=n_bins)
        axs[0].set_title('Countries we can detect both countries and methods', fontsize=6)
        axs[1].set_title('Countries we cannot detect countries or methods', fontsize=6)
        axs[0].set_xlabel('Year', fontsize=8)
        axs[0].set_ylabel('Number of papers', fontsize=8)
        #plt.show()
        plt.savefig(os.path.join(os.getcwd(), 'lda_html', 'Histogram comparison.png'), dpi=500)

    def find_review_required_journal(self):
        journals = {}
        for paper_id, value in self.data.items():
            if 'countries' not in value:
                if value['journal'] in journals:
                    journals[value['journal']] += 1
                else:
                    journals[value['journal']] = 1
        top_journals = sorted(journals.items(), key=operator.itemgetter(1), reverse=True)[:10]
        journal_names = [x[0] for x in top_journals]
        print(journal_names)

    def detection_performance(self):
        year_with_countries = [int(v['year']) for k, v in self.data.items() if 'countries' in v]
        year_wo_countries = [int(v['year']) for k, v in self.data.items() if 'countries' not in v]
        print('The size of corpus is ', len(self.data))
        print('The number of papers that we can detect countries is ', len(year_with_countries), len(year_with_countries) / len(self.data))
        print('The number of papers that we cannot detect countries is ', len(year_wo_countries))
        countries_list = [v['countries'] for k, v in self.data.items() if 'countries'in v]
        countries = []
        for c_list in countries_list:
            for c in c_list:
                countries.append(c)
        print(collections.Counter(countries))


if __name__ == '__main__':
    data = Metadata(PATH_METADATA)
    #data.year_histogram()
    data.compare_on_year()
    #data.detection_performance()
    #data.find_review_required_journal()
