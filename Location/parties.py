import csv
import pprint


def get_bar_party_data():
    """this function reads from a csv file and converts the data into a list of dictionaries.
     each item in the list is a dictionary of a specific location and the number of complaint calls
     it received in 2016"""

    bar_list = []
    with open('bar_locations.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            bar_dict = {'location_type': row[0],
                        'zip_code': row[1],
                        'city': row[2],
                        'borough': row[3],
                        'latitude': row[4],
                        'longitude': row[5],
                        'num_calls': row[6]}
            bar_list.append(bar_dict)
    return bar_list


def print_data(data):
    for entry in data:
        print(entry)
        pprint.pprint(entry)


def my_max(dictionary):
    return_dict = {'num_calls': 0, 'place': None}

    for k,v in dictionary.items():
        if int(v) > return_dict['num_calls']:
            return_dict['place'] = k
            return_dict['num_calls'] = int(v)
    return return_dict


def my_min(dictionary):
    return_dict = {'num_calls': float('Inf'), 'place': None}
    for k,v in dictionary.items():
        if k == 'Unspecified':
            continue
        if int(v) < return_dict['num_calls']:
            return_dict['place'] = k
            return_dict['num_calls'] = int(v)
    return return_dict


def get_most_noisy_city_and_borough(data):
    """ fill in the Nones for the dictionary below using the bar party data """
    noisiest_city_and_borough = {'city': None, 'borough': None, 'num_city_calls': None, 'num_borough_calls': None}
    aggregate_city = {}
    aggregate_borough = {}
    for item in data[1:]:
        aggregate_city.setdefault(item['city'], 0)
        aggregate_borough.setdefault(item['borough'], 0)
        aggregate_city[item['city']] += int(item['num_calls'])
        aggregate_borough[item['borough']] += int(item['num_calls'])

    noisiest_city_dict = my_max(aggregate_city)
    noisiest_borough_dict = my_max(aggregate_borough)
    noisiest_city_and_borough['city'] = noisiest_city_dict['place']
    noisiest_city_and_borough['num_city_calls'] = noisiest_city_dict['num_calls']
    noisiest_city_and_borough['borough'] = noisiest_borough_dict['place']
    noisiest_city_and_borough['num_borough_calls'] = noisiest_borough_dict['num_calls']
    return noisiest_city_and_borough


def get_quietest_city_and_borough(data):
    """ fill in the Nones for the dictionary below using the bar party data """

    quietest_city_and_borough = {'city': None, 'borough': None, 'num_city_calls': None, 'num_borough_calls': None}

    aggregate_city = {}
    aggregate_borough = {}
    for item in data[1:]:
        aggregate_city.setdefault(item['city'], 0)
        aggregate_borough.setdefault(item['borough'], 0)
        aggregate_city[item['city']] += int(item['num_calls'])
        aggregate_borough[item['borough']] += int(item['num_calls'])

    quietest_city_dict = my_min(aggregate_city)
    quietest_borough_dict = my_min(aggregate_borough)
    quietest_city_and_borough['city'] = quietest_city_dict['place']
    quietest_city_and_borough['num_city_calls'] = quietest_city_dict['num_calls']
    quietest_city_and_borough['borough'] = quietest_borough_dict['place']
    quietest_city_and_borough['num_borough_calls'] = quietest_borough_dict['num_calls']
    return quietest_city_and_borough


if __name__ == '__main__':
    bar_data = get_bar_party_data()

    # uncomment the line below to see what the data looks like
    #print_data(bar_data)

    noisy_metrics = get_most_noisy_city_and_borough(bar_data)

    quiet_metrics = get_quietest_city_and_borough(bar_data)

    print('Noisy Metrics: {}'.format(noisy_metrics))
    print('Quiet Metrics: {}'.format(quiet_metrics))
