#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format
"""
import sys
import os

import pandas as pd


import xlrd
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    header_dict = {}

    ### example on how you can get the data
    sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    # Get header row
    #print sheet_data[0]
    #print sheet_data[3]
    # Create dict to store header data. we can then access columns using names
    for index, header in enumerate(sheet_data[0]):
        header_dict[header] = index
    #print header_dict


    coast_data = [sheet.cell_value(row, header_dict['COAST']) for row in range(sheet.nrows)]
    #print coast_data[3]
    for index, coast_data_item in enumerate(coast_data):
        if index > 0:
            excel_time = xlrd.xldate_as_tuple(coast_data_item, 0)
            print excel_time

    coast_pd_data = pd.Series(coast_data[1:])

    maxvalue = coast_pd_data.max()
    minvalue = coast_pd_data.min()
    avgcoast = coast_pd_data.mean()
    maxtime = xlrd.xldate_as_tuple(maxvalue, 0)
    mintime = xlrd.xldate_as_tuple(minvalue, 0)

    #print "MAXTime", maxtime
    ### other useful methods:
    # print "\nROWS, COLUMNS, and CELLS:"
    # print "Number of rows in the sheet:",
    # print sheet.nrows
    # print "Type of data in cell (row 3, col 2):",
    # print sheet.cell_type(3, 2)
    # print "Value in cell (row 3, col 2):",
    # print sheet.cell_value(3, 2)
    # print "Get a slice of values in column 3, from rows 1-3:"
    # print sheet.col_values(3, start_rowx=1, end_rowx=4)

    # print "\nDATES:"
    # print "Type of data in cell (row 1, col 0):",
    # print sheet.cell_type(1, 0)
    # exceltime = sheet.cell_value(1, 0)
    # print "Time in Excel format:",
    # print exceltime
    # print "Convert time to a Python datetime tuple, from the Excel float:",
    # print xlrd.xldate_as_tuple(exceltime, 0)


    # data = {
    #         'maxtime': (0, 0, 0, 0, 0, 0),
    #         'maxvalue': 0,
    #         'mintime': (0, 0, 0, 0, 0, 0),
    #         'minvalue': 0,
    #         'avgcoast': 0
    # }

    data = {}

    data['maxtime'] = maxtime
    data['maxvalue'] = maxvalue
    data['mintime'] = mintime
    data['minvalue'] = minvalue
    data['avgcoast'] = avgcoast

    output_string_list = "maxtime maxvalue mintime minvalue avgcoast".split()
    for output in output_string_list:
        print "Value of {0} in data dict is {1}".format(output, data[output])

    return data


def test():
    open_zip(datafile)
    data = parse_file(datafile)

    assert round(data['maxvalue'], 10) == round(18779.02551, 10)
    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)



test()