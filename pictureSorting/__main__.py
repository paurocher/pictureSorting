from .modules.ui import main

import argparse


from .modules.ui import main
from .modules.utilities import reset_test_folders

parser = argparse.ArgumentParser(
    prog='PictureSorter',
    description='A program to organize pictures, move files, clean folders, ...',
    epilog='Text at the bottom of help'
)
parser.add_argument("-r", action="store_true")

args = parser.parse_args()
if args.r:
    reset_test_folders()
main.run()