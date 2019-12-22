# HW6 - Video Analysis - SHIH-YUAN WANG
#----------------------------------------------------------------------------------------------

import csv
import pprint

def get_video_data():
    """this function reads from a .csv file and converts the data into a list of dictionaries.
     each item in the list is a dictionary of a specific videos and their attributes."""

    vid_data = []
    with open('USvideos.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if len(row) == 16:
                vid_dict = {'video_id': row[0],
                            'trending_date': row[1],
                            'title': row[2],
                            'channel_title': row[3],
                            'category_id': row[4],
                            'publish_times': row[5],
                            'tags': row[6],
                            'views': row[7],
                            'likes': row[8],
                            'dislikes': row[9],
                            'comment_count': row[10],
                            'thumbnail_link': row[11],
                            'comments_disabled': row[12],
                            'ratings_disabled': row[13],
                            'video_error': row[14],
                            'description': row[15]
                            }
                vid_data.append(vid_dict)
    return vid_data


def print_data(data):
    for entry in data:
        pprint.pprint(entry)


def get_most(dictionary):
# get the most popular as well as most liked and disliked channel

    return_dict = {'channel_title': None, 'num_total': 0}
    for k,v in dictionary.items():
        if int(v) > return_dict['num_total']:
            return_dict['channel_title'] = k
            return_dict['num_total'] = int(v)
    return return_dict


def get_least(dictionary):
# get the least popular channel

    return_dict = {'channel_title': None, 'num_total': float('Inf')}
    for k,v in dictionary.items():
        if int(v) < return_dict['num_total']:
            return_dict['channel_title'] = k
            return_dict['num_total'] = int(v)
    return return_dict


def get_most_popular_and_least_popular_channel(data):
    """ fill in the Nones for the dictionary below using the vid data """
    # Output dictionary
    most_popular_and_least_popular_channel = {'most_popular_channel': None,
                                              'least_popular_channel': None,
                                              'most_pop_num_views': None,
                                              'least_pop_num_views': None}
    # Aggregate the number of views of each channel
    aggregate_channel = {}
    for item in data[1:]:
        aggregate_channel.setdefault(item['channel_title'], 0)         # check, create keys and set o as default value
        aggregate_channel[item['channel_title']] += int(item['views']) # update total views of the corresponding channel

    # Get the most popular channel in aggregate_channel dictionary
    most_popular_channel_dict = get_most(aggregate_channel)
    # Assign the value from most_popular_channel_dict to the output dictionary
    most_popular_and_least_popular_channel['most_popular_channel'] = most_popular_channel_dict['channel_title']
    most_popular_and_least_popular_channel['most_pop_num_views'] = most_popular_channel_dict['num_total']

    # Get the least popular channel in aggregate_channel dictionary
    least_popular_channel_dict = get_least(aggregate_channel)
    # Assign the value from least_popular_channel_dict to the output dictionary
    most_popular_and_least_popular_channel['least_popular_channel'] = least_popular_channel_dict['channel_title']
    most_popular_and_least_popular_channel['least_pop_num_views'] = least_popular_channel_dict['num_total']

    return most_popular_and_least_popular_channel


def get_most_liked_and_disliked_channel(data):
    """ fill in the Nones for the dictionary below using the vid data """
    # Output dictionary
    most_liked_and_disliked_channel = {'most_liked_channel': None,
                                       'num_likes': None,
                                       'most_disliked_channel': None,
                                       'num_dislikes': None}
    # Aggregate the number of likes and dislikes of each channel
    aggregate_channel_likes = {}
    aggregate_channel_dislikes = {}
    for item in data[1:]:
        aggregate_channel_likes.setdefault(item['channel_title'], 0)               # check, create keys and set o as default value in aggregate_channel_likes dic
        aggregate_channel_likes[item['channel_title']] += int(item['likes'])       # update total likes of the corresponding channel
        aggregate_channel_dislikes.setdefault(item['channel_title'], 0)            # check, create keys and set o as default value in aggregate_channel_dislikes dic
        aggregate_channel_dislikes[item['channel_title']] += int(item['dislikes']) # update total dislikes of the corresponding channel

    # Get the most liked channel in most_liked_channel_dict
    most_liked_channel_dict = get_most(aggregate_channel_likes)
    # Assign the value from most_liked_channel_dict to the output dictionary
    most_liked_and_disliked_channel['most_liked_channel'] = most_liked_channel_dict['channel_title']
    most_liked_and_disliked_channel['num_likes'] = most_liked_channel_dict['num_total']

    # Get the most disliked channel in most_disliked_channel_dict
    most_disliked_channel_dict = get_most(aggregate_channel_dislikes)
    # Assign the value from most_disliked_channel_dict to the output dictionary
    most_liked_and_disliked_channel['most_disliked_channel'] = most_disliked_channel_dict['channel_title']
    most_liked_and_disliked_channel['num_dislikes'] = most_disliked_channel_dict['num_total']

    return most_liked_and_disliked_channel


if __name__ == '__main__':
    vid_data = get_video_data()

    # uncomment the line below to see what the data looks like
    # print_data(vid_data)

    popularity_metrics = get_most_popular_and_least_popular_channel(vid_data)

    like_dislike_metrics = get_most_liked_and_disliked_channel(vid_data)

    print('Popularity Metrics: {}'.format(popularity_metrics))
    print('Like Dislike Metrics: {}'.format(like_dislike_metrics))
