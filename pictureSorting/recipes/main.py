"""
This file has the functions to run. The other files have the functions defined
but are there only to help the functions on this file to run.
This is the place to go to do everything:
    - move files
    - delete files
    - change exif data,
    - ...
    
Just uncomment the function and run this file (Shift+F10)
"""

import os
import sys
sys.path.append(os.path.abspath('../..'))
from pictureSorting.modules import (
    utilities,
    globals,
)
from pictureSorting.modules.heif_tools import (
    read_heif,
    heif_to_jpg,
    get_heif_file_metadata,
    heif_metadata_human_readable,
)
from pprint import pprint as pp
import shutil



"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""
# utilities.subdivide_folder_contents(
#     "/media/fuku/T7/Pictures/2022/03/17/",
#     500
# )
"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""


"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""
"""Move movie files to folders with a limit on the amount of files moved"""
# source_folder = "/media/fuku/T7/Movies/Personal_011"
# dest_folder = "/media/fuku/T7/Movies/Personal_001"
# limit = 4000
# for i, file in enumerate(utilities.scan_dir(source_folder)):
#     print(i)
#     if i >= 4000:
#         break
#     utilities.move_by_extension([".avi", ".mov", ".mpg"],
#                                 file,
#                                 dest_folder)
"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""


"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""
"""Move files based on their size"""
# temp_trash_path = "/media/fuku/T7/temp_trash"
# files = utilities.scan_dir("/media/fuku/T7/Pictures/")
# print("Found files:", len(files))
# print("Getting file sizes ...")
# failed = []
# for file in files:
#     file_size = os.stat(file).st_size / (1024 * 1024)
#     rounded_file_size = round(file_size, 3)
#     if rounded_file_size < 0.1:
#         try:
#             shutil.move(file, temp_trash_path)
#         except:
#             failed.append(file)
# print("Failed:")
# pp(failed)
"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""


"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""
"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""


"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""
"""Moves duplicates to a temp folder."""
"""REMEMBER TO HAVE THE FOLDER ORGANIZED FIRST:
    - NO SUBFOLDERS OTHER THAN YEAR/MONTHS/DAYS
    - NO IMAGES OUTSIDE A ../../DAY SUBFOLDER
IF IN DOUBT MOVE THE WHOLE YEAR TO A TEMP FOLDER AND RUN THE SCRIPT ABOVE TO
MOVE EVERY SINGLE IMAGE TO ITS CORRESPONDING FOLDER BASED ON THE DATE!!"""
# Improve this one with 3 dir fields: 2 to compare, the third one to move
#  duplicates to
# utilities.find_duplicates("/media/fuku/T7/Pictures/2022",
#                           "/media/fuku/T7/temp_trash_2022_2")
"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""


"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""
"""Move all files in a folder to trash bin."""
# source_path = "/media/fuku/T7/temp_trash_2016"
# trash_path = "/media/fuku/T7/.Trash-1000/files"
# files = os.scandir(source_path)
# total_files = len(os.listdir(source_path))
# for i, file in enumerate(files):
#     # print("\rMoving file {}/{} to {}".format(i, total_files, trash_path, end=""))
#     shutil.move(file.path, trash_path)
"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""


"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""


"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""



"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""
"""Print HEIF metadata."""
# source_folder = "/home/fuku/Desktop/100CANON/Activités de Noël"
#
# all_files = utilities.scan_dir(source_folder)
# heif_files = [file for file in all_files if
#     os.path.splitext(file)[1].lower() in [".heic", ".heif"]]
#
# for i, file in enumerate(heif_files):
#     heif_file = read_heif(file)
#     print(file)
#     heif_metadata_human_readable(heif_file, "EXIF DateTimeOriginal")
#     print("")
"""-----------------------------------------------------------------------------
-----------------------------------------------------------------------------"""

