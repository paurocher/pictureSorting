import os
from PIL import Image
import pyheif
import io
import exifread
from pprint import pprint as pp
from pictureSorting.modules import utilities


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


def heif_metadata_human_readable(heif_file, key=""):
    metadata = heif_file.metadata[0]["data"][6:]
    metadata = io.BytesIO(metadata)
    metadata = exifread.process_file(metadata, details=False)
    if key:
        metadata = metadata[key]
    pp(metadata)


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


