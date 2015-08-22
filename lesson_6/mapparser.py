#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the
tag name as the key and number of times this tag can be encountered in
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint

def get_root(fname):
    # Use iterparse, the thing no one taught us how to use.
    # http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree
    tree = ET.iterparse(fname)
    return tree

def count_tags(filename):
    count_tags_dict = dict()
    with open(filename, 'r') as fd:
        tree = get_root(fd)
        for event, elem in tree:
            if event == 'end':
                print("{} : {}".format(elem.tag, elem.text))
                # Use setdefault in case item has not been seen before, increment by 1 always
                count_tags_dict[elem.tag] = count_tags_dict.setdefault(elem.tag, 0) + 1
            elem.clear()
    pprint.pprint(count_tags_dict)
    return count_tags_dict

def test():

    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}



if __name__ == "__main__":
    test()