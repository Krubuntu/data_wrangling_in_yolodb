# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.

import xlrd
import os
import csv
from zipfile import ZipFile
from pprint import pprint as pprint

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"

REGION_LIST = "COAST EAST FAR_WEST NORTH NORTH_C SOUTHERN SOUTH_C WEST".split()

def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def calculate_region_stats(cv, sheet):

    maxval = max(cv)
    minval = min(cv)

    maxpos = cv.index(maxval) + 1
    minpos = cv.index(minval) + 1

    maxtime = sheet.cell_value(maxpos, 0)
    realtime = xlrd.xldate_as_tuple(maxtime, 0)
    mintime = sheet.cell_value(minpos, 0)
    realmintime = xlrd.xldate_as_tuple(mintime, 0)

    data = dict()

    data['maxtime'] = realtime
    data['maxvalue'] = maxval
    data['mintime'] = realmintime
    data['minvalue'] = minval
    data['avgcoast'] = sum(cv) / float(len(cv))

    return data


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    # Create dict to store header data. we can then access columns using names
    header_dict = {}
    for index, header in enumerate(sheet_data[0]):
        header_dict[header] = index
    #print(header_dict)

    data = dict()

    for region in REGION_LIST:
        output_stats_dict = dict()
        print region
        # This includes the *entire* column, excluding header row via range start value
        region_data = [sheet.cell_value(row, header_dict[region]) for row in range(1, sheet.nrows)]
        #print region_data
        region_stats_dict = calculate_region_stats(region_data, sheet)

        pprint(region_stats_dict)

        # Grab info we need to insert time data
        time_data = region_stats_dict['maxtime']
        #pprint(time_data)
        Year, Month, Day, Hour, _, _ = time_data

        region_max_val = region_stats_dict['maxvalue']
        print("region_max_value {}".format(region_max_val))
        output_stats_dict['Year'] = Year
        output_stats_dict['Month'] = Month
        output_stats_dict['Day'] = Day
        output_stats_dict['Hour'] = Hour
        output_stats_dict['Max Load'] = region_stats_dict['maxvalue']
        pprint(output_stats_dict)
        #print region_stats_dict
        # Add the stats dict to data dictionary using region as the key
        data[region] = output_stats_dict
        print

    pprint(data)
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    return data

def save_file(data, filename):
    # YOUR CODE HERE
    pass

def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    test()
