"""Move photos to directory with time of their creation"""

import argparse
import logging
import os
import shutil
from pathlib import Path
from time import strptime

import exifread

TAG_DATE_ORIGINAL = "EXIF DateTimeOriginal"
logging.getLogger("exifread").setLevel(logging.ERROR)  # Remove warnings

# Argument parsing
parser = argparse.ArgumentParser(
    description="copy/move picture files according to year/month of exif tag 'EXIF DateTimeOriginal' "
)
parser.add_argument(
    "-s",
    "--src_directory",
    help="source directory",
    required=False,
    default=os.getcwd(),
)
parser.add_argument(
    "-t",
    "--target_directory",
    help="target directory",
    required=False,
    default=os.getcwd(),
)
parser.add_argument(
    "-m",
    "--move",
    help="Move insted of copy",
    action="store_true",
)
argument = parser.parse_args()


# Check source and target directories
source_directory = Path(argument.src_directory)
if source_directory.exists() is False:
    print(f"Source directory ({source_directory}) does not exist.")
    exit()
target_directory = Path(argument.target_directory)
if target_directory.exists() is False:
    print(f"Target directory ({target_directory}) does not exist.")
    exit()

# Walk source directory
for path, subdirs, files in os.walk(source_directory):
    for name in files:
        if path == target_directory:
            continue
        image_path = os.path.join(path, name)
        # Check extension
        if image_path.endswith((".png", ".jpg")) is False:
            continue
        with open(image_path, "rb") as fh:
            # Read tag
            tags = exifread.process_file(fh, stop_tag=TAG_DATE_ORIGINAL)
            if TAG_DATE_ORIGINAL in tags:
                exif_creation_time = tags[TAG_DATE_ORIGINAL].values
                # Creation time
                CREATION_TIME = (
                    strptime(exif_creation_time, '%Y:%m:%d %H:%M:%S')
                    if TAG_DATE_ORIGINAL in tags
                    else None
                )
                if CREATION_TIME:
                    # Create directory
                    print(">>> Analyse de " + image_path)
                    CREATION_TIME_YEAR = str(CREATION_TIME.tm_year)
                    CREATION_TIME_MONTH = str(CREATION_TIME.tm_mon)
                    directory = os.path.join(
                        target_directory,
                        CREATION_TIME_YEAR,
                        (
                            "0" + CREATION_TIME_MONTH
                            if len(CREATION_TIME_MONTH) == 1
                            else CREATION_TIME_MONTH
                        ),
                    )
                    if os.path.exists(directory) is False:
                        os.makedirs(directory)
                        print(f"{directory} created")
                    # Copy/Move file
                    target = os.path.join(directory, name)
                    print(target)
                    if image_path != target:
                        if argument.move:
                            Path(image_path).rename(target)
                            print(f"Move {image_path} to {target}")
                        else:
                            shutil.copyfile(image_path, target)
                            print(f"Copy {image_path} to {target}")
            else:
                continue
