#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Let's assume that you combined the code from the previous 2 exercises
# with code from the lesson on how to build requests, and downloaded all the data locally.
# The files are in a directory "data", named after the carrier and airport:
# "{}-{}.html".format(carrier, airport), for example "FL-ATL.html".
# The table with flight info has a table class="dataTDRight".
# There are couple of helper functions to deal with the data files.
# Please do not change them for grading purposes.
# All your changes should be in the 'process_file' function
# This is example of the datastructure you should return
# Each item in the list should be a dictionary containing all the relevant data
# Note - year, month, and the flight data should be integers
# You should skip the rows that contain the TOTAL data for a year
# data = [{"courier": "FL",
#         "airport": "ATL",
#         "year": 2012,
#         "month": 12,
#         "flights": {"domestic": 100,
#                     "international": 100}
#         },
#         {"courier": "..."}
# ]
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os
import re

TOTAL = re.compile("TOTAL")

datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files

def conv_bs4_to_int(bs4_struct):
    bs4_struct_str = bs4_struct.replace(",", '')
    bs4_int = int(bs4_struct_str)
    return bs4_int

def process_file(f):
    """This is example of the data structure you should return.
    Each item in the list should be a dictionary containing all the relevant data
    from each row in each file. Note - year, month, and the flight data should be 
    integers. You should skip the rows that contain the TOTAL data for a year
    data = [{"courier": "FL",
            "airport": "ATL",
            "year": 2012,
            "month": 12,
            "flights": {"domestic": 100,
                        "international": 100}
            },
            {"courier": "..."}
    ]
    """
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-")
    
    with open("{}/{}".format(datadir, f), "r") as html:

        soup = BeautifulSoup(html)
        data_tdr_right = soup.find_all("table", class_='dataTDRight')
        my_count = 0

        # Iterate over table content, ignore leading "\n" leading row and trailing two rows.
        # Second to last row contains TOTAL td.
        for table_content in data_tdr_right[0].contents[2:]:
            try:
                if not re.search(TOTAL, table_content.contents[2].string):                   
                    my_count += 1
                    table_data_dict = dict()

                    table_data_dict["courier"] = info["courier"]
                    table_data_dict["airport"] = info["airport"]

                    #print("table_content", table_content)
                    #print("COUNT", my_count)

                    table_data_dict["year"] = conv_bs4_to_int(table_content.contents[1].string)
                    table_data_dict["month"] = conv_bs4_to_int(table_content.contents[2].string)

                    flight_dict = {"domestic": conv_bs4_to_int(table_content.contents[3].string),
                                   "international": conv_bs4_to_int(table_content.contents[4].string)}

                    table_data_dict["flights"] = flight_dict

                    print(table_data_dict)
                    data.append(table_data_dict)
            except AttributeError as ex:
                print("Error: ".format(ex))
    print("Count", my_count)
    return data

def test():
    print ("Running a simple test...")
    #open_zip(datadir)
    files = process_all(datadir)
    data = []
    for f in files:
        data += process_file(f)
        
    assert len(data) == 399  # Total number of rows
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["month"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    assert data[-1]["airport"] == "ATL"
    assert data[-1]["flights"] == {'international': 108289, 'domestic': 701425}
    
    print("... success!")

if __name__ == "__main__":
    test()