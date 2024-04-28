from exif import Image
from utilities import scan_dir, is_picture
import exiftool

def set_exif_tag_value(path, tag, value):
    """Sets the value to an exif tag
    :param tag:
    :param value:
    :return:
    """
    with open(path, "rb") as image_file:
        image = Image(image_file)

    image[tag] = value

    with open(path, "wb") as new_image_file:
        new_image_file.write(image.get_file())

    print("Picture {}\nTag {} set to {}".format(path, tag, value))


def read_exif(path):
    """Reads the exif of a given path.
    :param path:
    :return: dict
    """

    with open(path, "rb") as image_file:
        image = Image(image_file)

    if image.has_exif:
        image_members = dir(image)
        for index, image_member_list in enumerate(image_members):
            print("{}: {}".format(image_member_list, image.get(image_member_list)))
            return
    print("Image has no exif data.")


def exiftool_get(path):
    metadata = exiftool.ExifToolHelper().get_metadata(files=[path])
    # print("metadata", metadata)
    for d in metadata:
        for k, v in d.items():
            print(k, v)
        # print(d)

# read_exif("/media/fuku/T7/Pictures/2009/forest.jpg")
# read_exif("/media/fuku/T7/recupHanae/recup_dir.3/f3286944.jpg")

#
# set_exif_tag_value("/media/fuku/T7/Pictures/2009/forest.jpg", "image_description", "From Hanae's camera")
# set_exif_tag_value("/media/fuku/T7/recup_dir.3/f3286944.jpg", "image_description", "From Hanae's camera")

# pictures = scan_dir("/media/fuku/T7/recupHanae")
# for i, picture in enumerate(pictures):
#     print("Processing doc {} of {}".format(i, len(pictures)))
#     if is_picture(picture):
#         # set_exif_tag_value(picture, "image_description", "From Hanae's camera")
#         print(read_exif(picture))


image = ("/home/fuku/Desktop/100CANON/gphotos_pau/Takeout/Google Photos/Ice climbing "
  "01_03-2020/20200301_133929.jpg")
image2 = ("/home/fuku/Desktop/100CANON/gphotos_pau/Takeout/Google Photos/Ice climbing "
       "01_03-2020/20200301_133926.jpg")
exiftool_get(image)