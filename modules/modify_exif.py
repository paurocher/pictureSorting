from exif import Image
from MoveByExif import scan_dir, is_picture

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
    print("Image has no exif data.")

# read_exif("/media/fuku/T7/Pictures/2009/forest.jpg")
# read_exif("/media/fuku/T7/recupHanae/recup_dir.3/f3286944.jpg")

#
# set_exif_tag_value("/media/fuku/T7/Pictures/2009/forest.jpg", "image_description", "From Hanae's camera")
# set_exif_tag_value("/media/fuku/T7/recup_dir.3/f3286944.jpg", "image_description", "From Hanae's camera")

pictures = scan_dir("/media/fuku/T7/recupHanae")
for i, picture in enumerate(pictures):
    print("Processing doc {} of {}".format(i, len(pictures)))
    if is_picture(picture):
        # set_exif_tag_value(picture, "image_description", "From Hanae's camera")
        print(read_exif(picture))
