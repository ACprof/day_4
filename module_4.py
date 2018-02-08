'''
Created on 2018 M02 8

@author: Nuno
'''

import csv

COLUMN_EXPECTED = "EVIDENCE"

if __name__ == '__main__':

    file_name = "single_file.csv"
    file_name_result = "single_file_out.csv"

    index = -1
    with open(file_name, "r") as handle_in:
        with open(file_name_result, "w", newline="") as handle_out:
            reader = csv.reader(handle_in, delimiter=",", quotechar='"')
            csv_writer = csv.writer(
                handle_out, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row_header = []
            for row in reader:
                if (len(row_header) == 0):  # catch header
                    if (COLUMN_EXPECTED in row):
                        row_header = row
                        index = row_header.index(COLUMN_EXPECTED)
                        # save header
                        row_to_write = row[: index] + \
                            ["EV1", "EV2"] + row[index + 1:]
                        csv_writer.writerow(row_to_write)
                else:  # process lines
                    row_to_write = row[: index] + \
                        row[index].split(" ") + row[index + 1:]
                    # save new line
                    csv_writer.writerow(row_to_write)

    if (index == -1):
        print("File not supported")
    else:
        print("File saved")
