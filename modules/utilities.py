import shutil
import os
import re
from datetime import datetime
import globals
from pprint import pprint as pp
import exifread
from zlib import crc32
import ffmpeg
# from binascii import crc32

def scan_dir(path, recursive=True, documents=[]):
    """Scans a dir and outputs all documents paths.
    :param path: str
    :param recursive: Bool
    :return: list()
    """
    dir_contents = os.scandir(path)
    for element in dir_contents:
        if os.path.isdir(element):
            if recursive:
                scan_dir(element.path, True, documents)
        # documents.add(element.path)
        if os.path.isfile(element):
            documents.append(element.path)
    return documents
"""Changed documents from set() to list() so we can store duplicates"""


def move_by_extension(extensions, file, destination):
    """Moves a file to a destination
    :param extensions: list
    :param origin: str
    :param destination:v str
    :return: None
    """

    file_name = os.path.basename(file)
    dest_contents = [os.path.basename(file.path) for file in os.scandir(destination)]
    # pp(dest_contents)

    if file_name in dest_contents:
        print("A file with the same name exists in the destination folder")
        return
    for ext in extensions:
        if os.path.splitext(file)[1] == ext:
            # print(ext, file, destination)
            shutil.move(file, destination)


def delete_xmp_files(folder):
    files = list(scan_dir(folder))
    counter = 0
    for file in files:
        if os.path.splitext(file)[1].lower() in [".xmp"]:
            try:
                shutil.move(file, "/home/fuku/.local/share/Trash/files/")
                counter += 1
            except shutil.Error as error:
                print("File {} already exists in the trash.".format(file))
                continue
            print("Moved to trash:", file)
    print("Moved to trash {} files.".format(counter))



def is_picture(path):
    """Checks wether the given path is a picture or not.
    :param path: str
    :return: True / False
    """
    if os.path.splitext(path)[1] in globals.IMAGE_FORMATS:
        return True
    return False

def is_movie(path):
    """Checks wether the given path is a movie or not.
    Args:
        path: str

    Returns: Bool
    """
    if os.path.splitext(path)[1] in globals.VIDEO_FORMATS:
        return True
    return False


def get_file_dates(image_path):
    """Gets the exif dates of an image file.
    Args:
        image_path: str

    Returns: list
    """

    dates = []
    if os.path.isdir(image_path):
        return

    if is_movie(image_path):
        # print(image_path)
        probe = ffmpeg.probe(image_path)
        # pp(probe)
        creation_t = None
        # get creation time from metadata
        try:
            creation_t = probe["format"]["tags"]["creation_time"]
            # print(creation_t)
            dates.append(datetime.strptime(creation_t, "%Y-%m-%dT%H:%M:%S.%fZ"))
        except Exception as e:
            # print(e)
            # pp(probe)
            # print("\n\n\n\n\n")
            pass
        try:
            dates.append(datetime.fromtimestamp(os.path.getmtime(image_path)))
        except:
            pass
        try:
            dates.append(datetime.fromtimestamp(os.path.getctime(image_path)))
        except:
            pass
        try:
            dates.append(datetime.fromtimestamp(os.path.getatime(image_path)))
        except:
            pass
        return dates


    with open(image_path, 'rb') as image:
        try:
            tags = exifread.process_file(image)
            for tag, value in tags.items():
                if "date" in tag.lower():
                    if re.match("\d\d\d\d:\d\d:\d\d \d\d:\d\d:\d\d", str(value)):
                        dates.append(datetime.strptime(str(value), "%Y:%m:%d %H:%M:%S"))
        except Exception:
            pass
        try:
            dates.append(datetime.fromtimestamp(os.path.getctime(image_path)))
            dates.append(datetime.fromtimestamp(os.path.getmtime(image_path)))
            dates.append(datetime.fromtimestamp(os.path.getatime(image_path)))
        except:
            pass
    return dates


def get_earlier_date(dates):
    """Gets the earlier date from a set of dates
    :param date: list"""

    return min(dates)


def make_dest_path(date, movie=False):
    """Makes a destination folder path based on a date if that dest. path
    doesn't exist.
    Args:
        date: datetime.date
        movie: Bool

    Returns: str
    """
    media = "Pictures"
    if movie:
        media = "Movies/Personal"

    year = str(date.year)
    month = "{:0>2}".format(date.month)
    day = "{:0>2}".format(date.day)
    path = os.path.join("/media/fuku/T7/{}".format(media), year, month, day)

    if not os.path.exists(path):
        os.makedirs(path)
        print("created path:", path)

    return path


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


def seconds_to_date(seconds):
    return datetime.fromtimestamp(seconds).strftime("%A, %B %d, %Y %I:%M:%S")


def find_duplicates(path, trash="/media/fuku/T7/temp_trash"):
    """Checks if pictures in a folder has duplicates in the same folder by
    creating a Cyclic Redundancy Check (CRC32)

    Args:
        path: str: folder path
        trash: str: folder path

    Returns:
    """
    print("Scaning folder structure: {}".format(path))
    files = scan_dir(path)
    files_info = {}
    for i, file in enumerate(files):
        print("\rProcessing file: {} / {}".format(i+1, len(files)), end="")
        with open(file, 'rb') as image:
            size = os.stat(file).st_size / (1024 * 1024)
            crc = width = height = date = size = None
            crc = crc32(image.read())

        files_info[file] = {"CRC32": crc,
                            "width": width,
                            "height": height,
                            "exif_date": date,
                            "size": size}
    print("\nLooking for duplicates ...")
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
    print()
    print("Total files removed: {}".format(len(removed)))


def subdivide_folder_contents(src, max_files):
    """From a folder with lots of files, make sub-folders wih x amount of files.
    src: paths: str
    max_files: int
    """
    src_contents = utilities.scan_dir(src, recursive=False)
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


def find_hidden(paths=[]):
    """Outputs paths starting with "." from a list of paths.
    Args:
        paths: list
    Returns: dict: path: file_size
    """
    hidden_paths = {}
    for path in paths:
        if os.path.split(path)[-1].startswith("."):
            hidden_paths[path] = os.stat(path).st_size  / (1024 * 1024)
    hidden_paths_s = {k: v for k, v in sorted(hidden_paths.items(), key=lambda item: item[1])}
    return hidden_paths_s


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

"""Make a search and move for the mvies. Weĺl place them all in a separate
structure just like the one for the pictures: YYYY/MM/DD"""
