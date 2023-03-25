import utilities
import shutil
import os
import datetime
import re
from pprint import pprint as pp

black_list = []
files = utilities.scan_dir("/media/fuku/T7/Movies/Personal_001/")
for i, file in enumerate(files):
    if file in black_list:
        continue
    "/media/fuku/T7/Movies/Personal_001/ 20190410_000006.mp4"
    match = re.match("\d\d\d\d\d\d\d\d_\d\d\d\d\d\d.?", os.path.split(file)[-1])
    # print(match)
    if not match:
        continue
    print("\n", file)

    # dates = utilities.get_file_dates(file)
    # if len(dates) <= 3:
    #     continue
    # pp(dates)
    # smallest_date = utilities.get_earlier_date(dates)

    smallest_date = os.path.splitext(os.path.split(file)[-1])[0]
    smallest_date_a = smallest_date.split("_")[0]
    smallest_date_b = int("{}".format(smallest_date.split("_")[1]))
    if smallest_date_b > 59:
        continue
    smallest_date = "{}{}".format(smallest_date_a, str(smallest_date_b).zfill(6))
    print(smallest_date)
    smallest_date = datetime.datetime.strptime(smallest_date, "%Y%m%d%H%M%S")
    print(smallest_date)

    root_dest = utilities.make_dest_path(smallest_date, movie=True)
    file_name_dest = smallest_date.strftime("%Y%m%d_%H%M%S")

    # check if file with same name already exists
    exists = utilities.check_existing_filename(root_dest, file_name_dest)
    print(exists)
    extra_name = 0
    while exists:
        extra_name += 1
        file_name_dest = file_name_dest + "__{}" + extra_name
    full_new_file_path = os.path.join(root_dest,
                                      file_name_dest +
                                      os.path.splitext(os.path.split(file)[-1])[-1])
    print(full_new_file_path)
    shutil.move(file, full_new_file_path)
    print(i, " / ", len(files))

"1297"