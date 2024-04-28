"""Modify and read IPTC data."""
import iptcinfo3
from iptcinfo3 import IPTCInfo

import logging
iptcinfo_logger = logging.getLogger('iptcinfo')
iptcinfo_logger.setLevel(logging.ERROR)

def read_iptc_keywords(image):
    """Reads the IPTC data."""
    info = IPTCInfo(image, force=True)

    print(info["keywords"])
    return info["keywords"]

def write_iptc_keywords(image, keywords, append=True):
    info = IPTCInfo(image, force=True)
    if append:
        existing_keywords = [kw.decode('ASCII') for kw in info["keywords"]]
        clean_existing_keywords = set(existing_keywords + keywords)
        info["keywords"] = list(clean_existing_keywords)
    else:
        info["keywords"] = keywords
    info.save()
    info.save_as(image)
    read_iptc_keywords(image)

def remove_iptc_keyword(image, keyword):
    info = IPTCInfo(image, force=True)
    existing_keywords = [kw.decode('ASCII') for kw in info["keywords"]]
    if keyword in existing_keywords:
        existing_keywords.remove(keyword)
        info["keywords"] = existing_keywords
    else:
        print("This keyword does not exist.\n"
              "Available keywords: {}".format(existing_keywords))
    info.save()
    info.save_as(image)
    read_iptc_keywords(image)

def write_iptc_caption(image, caption):
    info = IPTCInfo(image, force=True)
    info["caption/abstract"] = caption
    info.save()
    info.save_as(image)


def read_iptc_caption(image):
    info = IPTCInfo(image, force=True)
    # print(help(info))
    print(info)
    # for k, v in info.items():
    #     print(k, v)
    # print(info["local "])
    return info["caption/abstract"]

image = ("/home/fuku/Desktop/100CANON/gphotos_pau/Takeout/Google Photos/Ice climbing "
  "01_03-2020/20200301_133929.jpg")
# read_iptc_keywords(image)
# write_iptc_keywords(image, ["Ice climbing"], append=True)
# remove_iptc_keyword(image, "caca")
read_iptc_caption(image)
# write_iptc_caption(image, "test of a caption")
