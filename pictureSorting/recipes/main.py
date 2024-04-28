"""
This file has the functions to run. The other files have the functions defined
but are there only to help the functions on this file to run.
This is the place to go to to do everything:
    - move files
    - delete files
    - change exif data,
    - ...
    
Jut uncomment the function and run this file (Shift+F10)
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
"""Move to trash .xmp files."""
# delete_xmp_files("/media/fuku/T7/Pictures")

"""Move to trash hidden files (starting with ".")"""
# source_folder = "/media/fuku/T7/Pictures/2022/"
# dest_folder = "/media/fuku/T7/hidden/"
# paths = utilities.scan_dir(source_folder)
# hidden_paths = utilities.find_hidden(paths)
# sizes = sorted([size for name, size in hidden_paths.items()])
#
# end = False
# while not end:
#     answer = input("""
# Display files and sizes: D
# Display sorted sizes: S
# Display max / min sizes: M
# Move all to dest folder: F
# End (do nothing): E
# """)
#     if answer == "D":
#         pp(hidden_paths)
#     if answer == "S":
#         pp(sizes)
#     if answer == "M":
#         print(max(sizes), min(sizes))
#     if answer =="F":
#         for path in hidden_paths:
#             print("implement a moving function to a folder that renames the "
#                   "file if another file in that folder with the same name already exists.")
#         end = True
#     if answer == "E":
#         end = True
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
"""Move image and movie files to appropriate location based on the date.
Rename duplicate files to force the relocation.
!!DO NOT RUN THIS IN ALREADY ORGANIZED BY DATE FOLDERS. OTHERWISE ALL FILES WILL 
HAVE __BIS__ APPENDED TO THEIR NAME!!!"""
# files = utilities.scan_dir("/home/fuku/Desktop/100CANON")
# DRY_RUN = False
#
# valid_formats = globals.IMAGE_FORMATS + globals.VIDEO_FORMATS
# renamed = []
# not_moved = []
# for i, file in enumerate(files):
#     print("\rProcessing file: {} / {}".format(i + 1, len(files)), end="")
#     if DRY_RUN:
#         print("\n  ", file)
#     if os.path.splitext(file)[1] not in valid_formats:
#         if DRY_RUN:
#             print("  not a valid format.\n\n", file)
#         continue
#     dates = utilities.get_file_dates(file)
#     if DRY_RUN:
#         print("  dates: ")
#         pp(dates)
#     if not dates:
#         print("No dates. Check code because there should at least be a date of"
#               "creation or some date!!")
#         continue
#     smallest_date = utilities.get_earlier_date(dates)
#     if DRY_RUN:
#         print("  smallest date: ", smallest_date)
#     movie = False
#     if os.path.splitext(file)[1] in globals.VIDEO_FORMATS:
#         movie = True
#     dest_path = utilities.make_dest_path(smallest_date, movie)
#     full_new_file_path = (os.path.join(
#         dest_path,
#         smallest_date.strftime("%Y%m%d_%H%M%S")
#         + os.path.splitext(
#             os.path.split(
#                 file)[-1]
#         )[-1]
#     )
#     )
#     if DRY_RUN:
#         print("  new file path: ", full_new_file_path)
#         print("DRY_RUN on. No files were moved.\n\n")
#
#     if not DRY_RUN:
#         try:
#             shutil.move(file, dest_path)
#         except:
#             path_parts = os.path.split(file)
#             file_parts = os.path.splitext(path_parts[-1])
#             new_file_name = "".join([file_parts[0], "__BIS__", file_parts[1]])
#             new_file_dest_path = os.path.join(dest_path, new_file_name)
#             try:
#                 shutil.move(file, new_file_dest_path)
#                 renamed.append([file, new_file_dest_path])
#             except:
#                 not_moved.append(file)
#                 continue
#             # print()
# if renamed:
#     pp(renamed)
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
"""Convert HEIF to JPG."""
# source_folder = "/home/fuku/Desktop/100CANON"
#
# all_files = utilities.scan_dir(source_folder)
# heif_files = [file for file in all_files if
#     os.path.splitext(file)[1].lower() in [".heic", ".heif"]]
#
# for i, file in enumerate(heif_files):
#     heif_file = read_heif(file)
#
#     new_file_name = os.path.split(file)
#     new_file_name_ext = os.path.splitext(new_file_name[-1])
#     new_file_name = "{}_fromHEIF.jpg".format(new_file_name_ext[0])
#     dest_path = os.path.join(os.path.split(file)[0], new_file_name)
#     print("{}/{}  {} --> {}".format(
#         i,
#         len(heif_files),
#         file,
#         dest_path)
#     )
#     heif_to_jpg(heif_file, dest_path)
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

