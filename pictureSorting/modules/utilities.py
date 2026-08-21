import copy
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from pprint import pprint as pp
from typing import List, Dict, Any, Tuple
from zlib import crc32
import exifread
import ffmpeg
import logging
import os
import re
import shutil
import subprocess
# from binascii import crc32

from Qt.QtWidgets import (
    QFileDialog,
)

from pictureSorting.modules import globals as glb


# This stops the exifread.process_file output on the terminal
#  If it messes up other logs I need I can move this to where
#  exifread.process_file happens.
logging.basicConfig(level=logging.ERROR)


def check_existing_filename(folder, file_name):
    """Checks if a file with the same name and extension already exists in the
    folder.
    Args:
        folder: str
        file_name: str

    Returns: Bool
    """

    contents = os.listdir(folder)
    if file_name in contents:
        return True
    return False



# def delete_xmp_files(folder):
#     files = list(scan_dir(folder))
#     counter = 0
#     for file in files:
#         if os.path.splitext(file)[1].lower() in [".xmp"]:
#             try:
#                 shutil.move(file, "/home/fuku/.local/share/Trash/files/")
#                 counter += 1
#             except shutil.Error as error:
#                 print("File {} already exists in the trash.".format(file))
#                 continue
#             print("Moved to trash:", file)
#     print("Moved to trash {} files.".format(counter))


def find_duplicates(path, trash="/media/fuku/T7/temp_trash"):
    """Checks if pictures in a folder has duplicates in the same folder by
    creating a Cyclic Redundancy Check (CRC32)

    Args:
        path: str: folder path
        trash: str: folder path

    Returns:
    """
    # print("Scaning folder structure: {}".format(path))
    files = scan_dir(path)
    files_info = {}
    for i, file in enumerate(files):
        # print("\rProcessing file: {} / {}".format(i+1, len(files)), end="")
        with open(file, 'rb') as image:
            size = os.stat(file).st_size / (1024 * 1024)
            crc = width = height = date = size = None
            crc = crc32(image.read())

        files_info[file] = {"CRC32": crc,
                            "width": width,
                            "height": height,
                            "exif_date": date,
                            "size": size}
    # print("\nLooking for duplicates ...")
    removed = []
    for i, (file, values) in enumerate(files_info.items()):
        # print("\rLooking for duplicates {}".format("." * (i % 20)), end="")
        if file in removed:
            continue
        crc = values["CRC32"]
        for search_file, search_values in files_info.items():
            if search_file == file:
                continue
            if search_values["CRC32"] == crc:
                # print("Moving to trash: {}".format(file))
                try:
                    shutil.move(search_file, trash)
                except:
                    path_parts = os.path.split(search_file)
                    file_parts = os.path.splitext(path_parts[-1])
                    new_file_name = "".join([file_parts[0], "__BIS__", file_parts[1]])
                    new_file_dest_path = os.path.join(*path_parts[:-1], new_file_name)
                    try:
                        shutil.move(new_file_dest_path, trash)
                        # renamed.append([file, new_file_dest_path])
                    except:
                        continue


                removed.append(search_file)
    # print()
    # print("Total files removed: {}".format(len(removed)))


def get_all_dst_dir_paths() -> list:
    """Get all dst dir file paths as a list"""
    # DONE on tab01: move to tab.py
    files = scan_dir(glb.DEST_DIR, True, None)
    glb.DEST_DIR_FILES = list(files.keys())


def get_earlier_date(dates: dict) -> datetime:
    """Gets the earlier date from a set of dates
    Args:
         date (dict): {'last_modif': datetime,
            'metadata_change': datetime,
            'last_access': datetime,
            ...}
    Returns:
        datetime: The earlier date
"""
    dates = [date for k, date in dates.items()]
    return min(dates)


def get_file_dates(image_path: Path, media_type):
    """Gets the exif dates of an image file.

    Pass "picture" as media type for any type of file other than movie.

    Args:
        image_path (Path):
        media_type (str): "videos" or "pictures"

    Returns: dict
    """
    dates = {}

    if media_type == "videos":
        probe = ffmpeg.probe(image_path)
        # pp(probe)
        creation_t = None
        # get creation time from metadata
        try:
            creation_t = probe["format"]["tags"]["creation_time"]
            # print(creation_t)
            dates["exif"] = (datetime.strptime(creation_t, "%Y-%m-%dT%H:%M:%S.%fZ"))
        except Exception as e:
            # print(e)
            # pp(probe)
            # print("\n\n\n\n\n")
            pass
        try:
            # last modification date from file
            dates["last_modif"] = (
                datetime.fromtimestamp(image_path.stat().st_mtime)
            )
        except:
            pass
        try:
            # time of the last metadata change
            dates["metadata_change"] = (
                datetime.fromtimestamp(image_path.stat().st_ctime)
            )
        except:
            pass
        try:
            # time of last access
            dates["last_access"] = (
                datetime.fromtimestamp(image_path.stat().st_atime)
                    )
        except:
            pass
        return dates

    elif media_type == "pictures":
        with open(image_path, 'rb') as image:
            try:
                tags = exifread.process_file(image)
                for tag, value in tags.items():
                    if "date" in tag.lower():
                        if re.match(
                                "\d\d\d\d:\d\d:\d\d \d\d:\d\d:\d\d",
                                str(value)
                        ):
                            dates["exif"] = (
                                datetime.strptime(str(value),
                                                  "%Y:%m:%d %H:%M:%S")
                            )
            except Exception:
                pass
            try:
                dates["last_modif"] = (
                    datetime.fromtimestamp(image_path.stat().st_mtime)
                )
                dates["metadata_change"] = (
                    datetime.fromtimestamp(image_path.stat().st_ctime)
                )
                dates["last_access"] = (
                    datetime.fromtimestamp(image_path.stat().st_atime)
                )
            except:
                pass
        return dates


def get_formats(path, formats=set()):
    """Gets a list of formats from a path and its recursive contents.
    :param path:
    :param formats:
    :return:
    """
    dir_contents = os.scandir(path)
    formats = formats
    for element in dir_contents:
        if element.is_dir():
            get_formats(element.path, formats)
        elif element.is_file():
            formats.add(os.path.splitext(element.path)[1])
    return formats


def get_size(path):
    """Get the size of a file in MB."""
    return round(path.stat().st_size  / (1024 * 1024), 4)


def is_movie(path: Path):
    """Checks whether the given path is a movie or not.
    Args:
        path: str

    Returns: bool
    """
    if path.suffix in glb.VIDEO_FORMATS:
        return True
    return False


def is_picture(path: Path):
    """Checks whether the given path is a picture or not.

    Args:
        path:

    Returns: bool
    """
    if path.suffix in glb.IMAGE_FORMATS:
        return True
    return False


def filter_by_extension(files: dict, extensions: list):
    """Filter out paths that do not have the specified extensions.

        Args:
            files (dict): {path: ...}
            extensions: list of extensions to filter by
    """
    selected = {}

    for path, v in files.items():
        # Remove the dot before the extension
        if path.suffix[1:].lower() in extensions:
            selected.update({path: v})
    return selected


def reset_test_folders():
    """Reset the test folders.

    Will be triggered if the module is run with the -r flag"""
    print("Resetting test folders")

    command = "/home/fuku/Desktop"
    print("  ", command)
    os.chdir(command)

    command = ["rm", "-rf", "test", "test_trash"]
    print("  ", command)
    subprocess.run(command)

    command = ["cp", "-r", "test_backup", "test"]
    print("  ", command)
    subprocess.run(command)

    command = ["cp", "-r", "test_trash_backup", "test_trash"]
    print("  ", command)
    subprocess.run(command)


def seconds_to_date(seconds):
    return datetime.fromtimestamp(seconds).strftime("%A, %B %d, %Y %I:%M:%S")


def subdivide_folder_contents(src, max_files):
    """From a folder with lots of files, make sub-folders wih x amount of files.
    Args:
        src: paths: str
        max_files: int
    """
    src_contents = scan_dir(src, recursive=False)
    print(len(src_contents))
    # print(src_contents)

    folder_counter = 0
    for i, file in enumerate(src_contents):
        # print(i % 3 + 1)
        if i % max_files == 0:
            folder_counter += 1
            sub_folder = "/".join([*os.path.split(src)[:-1], str(folder_counter)])
            os.makedirs(sub_folder)
        shutil.move(file, sub_folder)



"""Make a search and move for the movies. Weĺl place them all in a separate
structure just like the one for the pictures: YYYY/MM/DD"""
