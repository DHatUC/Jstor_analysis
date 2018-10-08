import os
import json


input_path = os.path.join(os.getcwd(), 'temp', 'country_region_list.csv')
output_path = os.path.join(os.getcwd(), 'temp', 'country_region.json')


def main():
    country_dict = {}
    stop_list = []
    with open(input_path) as f:
        for line in f:
            cells = line.split('\n')[0].split('\t')
            if len(cells[0]) > 0:
                country = cells[0]
            for region in cells[1:]:
                if ':' in region:
                    region_name = region.split(':')[1].strip()
                elif '()' in region:
                    region_name  = region.split('(')[0].split()
                else:
                    region_name = region.strip()
                if len(region_name) and all(x.isalpha() or x.isspace() for x in region_name):
                    if region_name not in country_dict:
                        country_dict[region_name] = country
                    else:
                        if country != country_dict[region_name]:
                            if region_name not in stop_list:
                                stop_list.append(region_name)
    for word in stop_list:
        del country_dict[word]
    with open(output_path, 'w') as f:
        json.dump(country_dict, f)


if __name__ == '__main__':
    main()