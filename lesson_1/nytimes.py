#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This exercise shows some important concepts that you should be aware about:
- using codecs module to write unicode files
- using authentication with web APIs
- using offset when accessing web APIs

To run this code locally you have to register at the NYTimes developer site
and get your own API key. You will be able to complete this exercise in our UI without doing so,
as we have provided a sample result.

Your task is to process the saved file that represents the most popular (by view count)
articles in the last day, and return the following data:
- list of dictionaries, where the dictionary key is "section" and value is "title"
- list of URLs for all media entries with "format": "Standard Thumbnail"

All your changes should be in the article_overview function.
The rest of functions are provided for your convenience, if you want to access the API by yourself.
"""
import json
import codecs
import requests
import os
import sys
import pprint

print(os.environ['NYTIMES_POPULAR_API_KEY'])

nyt_popular_key = os.environ['NYTIMES_POPULAR_API_KEY']
nyt_article_key = os.environ['NYTIMES_ARTICLE_API_KEY']



URL_MAIN = "http://api.nytimes.com/svc/"
URL_POPULAR = URL_MAIN + "mostpopular/v2/"
#URL_POPULAR = URL_MAIN + "mostpopular/v2/mostviewed/all-sections/1.json"
API_KEY = {"popular": nyt_popular_key,
            "article": nyt_article_key}


def get_from_file(kind, period):
    filename = "popular-{0}-{1}-full.json".format(kind, period)
    with open(filename, "r") as f:
        return json.loads(f.read())


def find_thumbnails_in_article(data_struct, results_list):
    if isinstance(data_struct, dict):
        #print("We have a dict")
        # pprint.pprint(data_struct)
        if 'format' in data_struct and 'url' in data_struct and \
                        data_struct['format'] == "Standard Thumbnail":
            results_list.append(data_struct['url'])

        for dict_value in data_struct.values():
            find_thumbnails_in_article(dict_value, results_list)

    elif isinstance(data_struct, list):
        #print("We have a list")
        # pprint.pprint(data_struct)
        for list_item in data_struct:
            find_thumbnails_in_article(list_item, results_list)

    return results_list



def article_overview(kind, period):
    data = get_from_file(kind, period)
    titles = []
    urls =[]
    # YOUR CODE HERE
    for article in data:
        titles.append({article['section']: article['title']})
        #pprint.pprint(titles)
        urls = find_thumbnails_in_article(article, urls)
    pprint.pprint(len(urls))

    return titles, urls


def query_site(url, target, offset):
    # This will set up the query with the API key and offset
    # Web services often use offset parameter to return data in small chunks
    # NYTimes returns 20 articles per request, if you want the next 20
    # You have to provide the offset parameter
    if API_KEY["popular"] == "" or API_KEY["article"] == "":
        print ("You need to register for NYTimes Developer account to run this program.")
        print ("See Instructor notes for information")
        return False
    params = {"api-key": API_KEY[target], "offset": offset}
    print("Params: {0}".format(params))
    r = requests.get(url, params=params)

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def get_popular(url, kind, days, section="all-sections", offset=0):
    # This function will construct the query according to the requirements of the site
    # and return the data, or print an error message if called incorrectly
    if days not in [1,7,30]:
        print ("Time period can be 1,7, 30 days only")
        return False
    if kind not in ["viewed", "shared", "emailed"]:
        print ("kind can be only one of viewed/shared/emailed")
        return False

    url = URL_POPULAR + "most{0}/{1}/{2}.json".format(kind, section, days)
    data = query_site(url, "popular", offset)

    return data


def save_file(kind="viewed", period=1):
    # This will process all results, by calling the API repeatedly with supplied offset value,
    # combine the data and then write all results in a file.
    data = get_popular(URL_POPULAR, kind, period)
    num_results = data["num_results"]
    full_data = []
    with codecs.open("popular-{0}-{1}-full.json".format(kind, period), encoding='utf-8', mode='w') as v:
        for offset in range(0, num_results, 20):
            data = get_popular(URL_POPULAR, kind, period, offset=offset)
            full_data += data["results"]

        v.write(json.dumps(full_data, indent=2))


def test():
    titles, urls = article_overview("viewed", 1)
    assert len(titles) == 20
    assert len(urls) == 30
    assert titles[2] == {'Opinion': 'Professors, We Need You!'}
    assert urls[20] == 'http://graphics8.nytimes.com/images/2014/02/17/sports/ICEDANCE/ICEDANCE-thumbStandard.jpg'


if __name__ == "__main__":
    #save_file()
    test()
