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
import pprint

datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files


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
    info = dict()
    info["courier"], info["airport"] = f[:6].split("-")

    with open("{}/{}".format(datadir, f), "r") as html:

        soup = BeautifulSoup(html)
        data_tdr_right = soup.find_all("table", class_='dataTDRight')
        #print(data_tdr_right)
        trailing_offset = len(data_tdr_right[0].contents) - 2
        for table_content in data_tdr_right[0].contents[2:trailing_offset]:
            table_data_dict = dict()

            table_data_dict["courier"] = info["courier"]
            table_data_dict["airport"] = info["airport"]
            table_data_dict["year"] = table_content.contents[1].string
            table_data_dict["month"] = table_content.contents[2].string

            flight_dict = {"domestic": table_content.contents[3].string,
                           "international": table_content.contents[4].string}

            table_data_dict["flights"] = flight_dict
            print(table_data_dict)
            #for ind_content in table_content.contents[1:-1]:
            #   print("ind content", ind_content)
            #print("table content",table_content.contents)
            #print ("Year", year)
            print("*" * 30)

            #flight_dict = {"domestic": table_content[3].string,
            #               "international": table_content[4].string}
            #info["flights"] = flight_dict
            #print(info)

            data.append(table_data_dict)

    pprint.pprint(data)
    return data


def test():
    print ("Running a simple test...")
    #open_zip(datadir)
    files = process_all(datadir)
    data = []
    for f in files:
        data += process_file(f)
    print("len(data)", len(data))
    assert len(data) == 399  # Total number of rows
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["month"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    assert data[-1]["airport"] == "ATL"
    assert data[-1]["flights"] == {'international': 108289, 'domestic': 701425}

    print ("... success!")

if __name__ == "__main__":
    test()