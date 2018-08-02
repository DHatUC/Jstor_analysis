from matplotlib import pyplot as plt
import json
import os
import collections
import sys

COUNTRY_CUTTOFF = int(sys.argv[1])

with open(os.path.join(os.getcwd(), 'metadata', 'countries_METHOD', 'method_countries.json')) as f:
    data = json.load(f)

filtered_data = {}
for key, countries in data.items():
    temp = {}
    for country, count in countries.items():
        if count >= COUNTRY_CUTTOFF:
            temp[country] = count
    if temp:
        filtered_data[key] = temp

num_countries = []
num_country_all = []
for key, countries in filtered_data.items():
    num_countries.append(len(countries))
    num_country_all.append(sum([int(v) for k, v in countries.items()]))
fig, axs = plt.subplots(1, 2, sharey= True, tight_layout=True)
print('Num of countries', collections.Counter(num_countries))
print()
print('Num of presence', collections.Counter(num_country_all))

n_bins = range(20)
axs[0].hist(num_countries, bins=n_bins)
axs[1].hist(num_country_all, bins=n_bins)
axs[0].set_title('Histogram of number of countries')
axs[1].set_title('Histogram of number of country name presence')
plt.show()


