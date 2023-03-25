import os
import io
import exifread
from PIL import Image
import pyheif
from pprint import pprint as pp
import utilities


def read_heif(path):
    heif_file = pyheif.read(path)

    return heif_file


def get_heif_file_metadata(heif_file):
    metadata = heif_file.metadata[0]["data"]
    # metadata = io.BytesIO(heif_file.metadata[0]["data"][6:])
    # metadata = exifread.process_file(metadata, details=False)
    # for k, v in metadata.items():
    #     print(k, v)
    return metadata


def heif_to_jpg(heif_file, save_path):
    metadata = get_heif_file_metadata(heif_file)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
        )

    # image.save(save_path, "JPEG", exif=metadata)
    image.save(save_path, "JPEG", quality=95, exif=metadata)

source_folder = "/media/fuku/T7/Pictures/2022"
all_files = utilities.scan_dir(source_folder)
heif_files = [file for file in all_files if os.path.splitext(file)[1].lower() in [".heic", ".heif"]]
pp(heif_files)

for i, file in enumerate(heif_files):
    heif_file = read_heif(file)

    new_file_name = os.path.split(file)
    new_file_name_ext = os.path.splitext(new_file_name[-1])
    new_file_name = "{}_fromHEIF.jpg".format(new_file_name_ext[0])
    dest_path = os.path.join(os.path.split(file)[0], new_file_name)
    print("{}/{}  {} --> {}".format(i,
                                          len(heif_files),
                                          file,
                                          dest_path))
    heif_to_jpg(heif_file, dest_path)
