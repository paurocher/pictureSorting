import sys
import os
from pprint import pprint as pp

sys.path.append(os.path.abspath('../..'))
from pictureSorting.modules import utilities

"""
1 scan folders and subfolders
2 check for picture or movie dates
3 print
"""

import argparse
parser=argparse.ArgumentParser(description="Get dates from picture and movies.")
parser.add_argument("folder", help="folder to scan")
args=parser.parse_args()


folder = args.folder
print("folder:")
print(args.folder)
print("end folder")
folder = folder.split("\n")[0]
print(folder)



print("Scanning folder: {}".format(folder))
files = utilities.scan_dir(folder)
for file in files:
    if utilities.is_picture(file):
        exif_date = utilities.get_file_dates(file)
        if exif_date.get("exif_date"):
            print(os.path.basename(file),"  \u001b[42m")
            pp(exif_date)
            print("\u001b[0m\n")
        else:
            print(os.path.basename(file),"  \u001b[41m")
            pp(exif_date)
            print("\u001b[0m\n")
    if utilities.is_movie(file):
        print("  ", os.path.basename(file))
        exif_date = utilities.get_file_dates(file)
        print("  \u001b[42m", exif_date, "\u001b[0m")
        print("")
