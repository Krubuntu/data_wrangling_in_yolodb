"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same


- if the value of the field is a valid year in range, as described above,
  write that line to the output_good file

- if the value of the field is not a valid year,
  write that line to the output_bad file

- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint
import re

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

DBPEDIA_PATTERN = re.compile('^http://dbpedia.org/')


def get_trunc_year(year_string):
    return int(year_string.split("-")[0])


def year_in_range(year):
    return 1886 < year <= 2014


def process_file(input_file, output_good, output_bad):

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        #COMPLETE THIS FUNCTION
        # Be lazy and efficient. I could store values in memory, but that may
        # get crazy if file is huge.
        good_fd = open(output_good, 'w')
        good_writer = csv.DictWriter(good_fd, delimiter=",", fieldnames=header)
        good_writer.writeheader()

        bad_fd = open(output_bad, 'w')
        bad_writer = csv.DictWriter(bad_fd, delimiter=",", fieldnames=header)
        bad_writer.writeheader()

        for row in reader:
            prod_start_year = row["productionStartYear"]
            uri = row["URI"]
            if re.match(DBPEDIA_PATTERN, uri):
                try:
                    truncated_year = get_trunc_year(prod_start_year)
                    if year_in_range(truncated_year):
                        print("Good year: {}".format(truncated_year))
                        row["productionStartYear"] = truncated_year
                        good_writer.writerow(row)
                    else:
                        print("Bad year: {}".format(truncated_year))
                        bad_writer.writerow(row)
                except Exception as ex:
                    print("Not able to truncate year: {}".format(ex))
                    bad_writer.writerow(row)
                #pprint.pprint(prod_start_year)
            else:
                pprint.pprint("Skipped row: {}".format(prod_start_year))
        good_fd.close()
        bad_fd.close()
    # This is just an example on how you can use csv.DictWriter
    # Remember that you have to output 2 files
    # with open(output_good, "w") as g:
    #     writer = csv.DictWriter(g, delimiter=",", fieldnames=header)
    #     writer.writeheader()
    #     for row in YOURDATA:
    #         writer.writerow(row)


def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()
