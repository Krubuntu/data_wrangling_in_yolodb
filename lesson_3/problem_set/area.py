#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the "areaLand" field,
you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it has to return a float
representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you like, but changes to process_file
will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'


def castable(input_string, input_type):
    '''
    Function to check the ability convert input_string into input_type via cast.

    :param input_string: String containing the value we wish to attempt casting.
    :param input_type: Targeted type into which we wish to cast.
    :return: True or False, depending on ability to cast input_string into input_type's type.
    '''
    try:
        return isinstance(input_type(input_string), input_type)
    except ValueError:
        return False


def audit_row(input_string):
    '''
    Function to audit rows in input file and assess the type of field values.

    :param input_string:
    :return: We return actual "types," not strings representing types:
            'list', NoneType, 'int', 'float', or catchall 'str.'
    '''
    if input_string.startswith("{"):
        return list
    elif len(input_string) == 0 or input_string == "NULL":
        # We use type(None) since it does not appear possible to 'return NoneType'
        return type(None)
    elif castable(input_string, float):
        if castable(input_string, int):
            return int
        else:
            return float
    else:
        return str

    
def fix_area(area):

    # YOUR CODE HERE
    #print("Area:{}".format(area))
    if type([]) == audit_row(area):
        clean_area = area.replace("{", "").replace("}", "")
        first_area, second_area = clean_area.split("|")
        print("First: {} Second: {}".format(first_area, second_area))
    else:
        pass
    return area



def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        #skipping the extra metadata
        for i in range(3):
            l = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,8):
        pprint.pprint(data[n]["areaLand"])

    assert data[3]["areaLand"] == None        
    assert data[8]["areaLand"] == 55166700.0
    assert data[20]["areaLand"] == 14581600.0
    assert data[33]["areaLand"] == 20564500.0    


if __name__ == "__main__":
    test()