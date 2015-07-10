#!/usr/bin/env python3
import sys
import os
import pprint


def find_thumbnails_in_article(data_struct, results_list):
    if isinstance(data_struct, dict):
        print("We have a dict")
        # pprint.pprint(data_struct)
        if 'format' in data_struct and 'url' in data_struct and \
                        data_struct['format'] == "Standard Thumbnail":
            results_list.append(data_struct['url'])

        for dict_value in data_struct.values():
            find_thumbnails_in_article(dict_value, results_list)

    elif isinstance(data_struct, list):
        print("We have a list")
        # pprint.pprint(data_struct)
        for list_item in data_struct:
            find_thumbnails_in_article(list_item, results_list)

    return results_list


def main():
    test_ds = [{'format': 'mediumThreeByTwo440',
                'height': 293,
                'url': 'http://static01.nyt.com/images/2015/07/04/us/04commutations-web/04commutations-web-mediumThreeByTwo440.jpg',
                'width': 440},
               {'format': 'Standard Thumbnail',
                'height': 75,
                'url': 'http://static01.nyt.com/images/2015/07/04/us/04commutations-web/04commutations-web-thumbStandard.jpg',
                'width': 75},
               {'format': 'Standard Thumbnail', 'url': 'http://foobar',
                'nested': {'format': 'Standard Thumbnail', 'url': 'http://foobaz'}}, ]
    results_list = []

    results = find_thumbnails_in_article(test_ds, results_list)
    print("Results: {}".format(results))


if __name__ == "__main__":
    main()
