#!/usr/bin/env python
# -*- coding: utf-8 -*-
# All your changes should be in the 'extract_airports' function
# It should return a list of airport codes, excluding any combinations like "All"

from bs4 import BeautifulSoup
html_page = "options.html"
import re

ALL_PATTERN = re.compile("^All")


def extract_airports(page):
    data = []
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html)
        airport_list = soup.find(id="AirportList")
        #print(airport_list)
        for airport in airport_list.find_all('option'):
            airport_value = airport.get("value")
            if not re.match(ALL_PATTERN, airport_value):
                data.append((airport_value))

    return data


def test():
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

test()