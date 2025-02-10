"""Move or copy photos to directories based on their creation time."""

import argparse
import logging
import os
import shutil
from pathlib import Path
from time import strptime, struct_time
from typing import Set
import exifread

TAG_DATE_ORIGINAL = "EXIF DateTimeOriginal"
logging.getLogger("exifread").setLevel(logging.ERROR)  # Remove warnings

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Copy/move picture files according to year/month of EXIF tag 'EXIF DateTimeOriginal'."
    )
    parser.add_argument(
        "-s",
        "--src_directory",
        help="Source directory",
        required=False,
        default=os.getcwd(),
    )
    parser.add_argument(
        "-t",
        "--target_directory",
        help="Target directory",
        required=False,
        default=os.getcwd(),
    )
    parser.add_argument(
        "--move",
        help="Move instead of copy",
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        help="Debug",
        action="store_true",
    )
    return parser.parse_args()

def check_directory(directory: Path, create_if_not_existing = False) -> None:
    """Check if the directory exists."""
    if not directory.exists():
        if create_if_not_existing:
            directory.mkdir(parents=True)
        else:
            print(str(directory) + " does not exists.")
            exit()

def get_creation_time(image_path) -> struct_time|None :
    """Get the creation time from the EXIF data of the image."""
    with open(image_path, "rb") as fh:
        tags = exifread.process_file(fh, stop_tag=TAG_DATE_ORIGINAL)
        if TAG_DATE_ORIGINAL in tags:
            exif_creation_time = tags[TAG_DATE_ORIGINAL].values
            return strptime(exif_creation_time, '%Y:%m:%d %H:%M:%S')
    return None

def create_directory(target_directory : Path, creation_time : struct_time) -> Path:
    """Create the target directory based on the creation time."""
    creation_time_year = str(creation_time.tm_year)
    creation_time_month = f"{creation_time.tm_mon:02d}"
    directory = target_directory / creation_time_year / creation_time_month
    check_directory(directory, True)
    return directory

def process_image(image_path: Path, target_directory: Path, move: bool) -> None:
    """Process the image by moving or copying it to the target directory."""
    creation_time = get_creation_time(image_path)
    if creation_time:
        directory = create_directory(target_directory, creation_time)
        target = directory / image_path.name
        print(f" --> Target: {target}")
        if target.exists():
            print("Target already existing")
            return
        if image_path != target:
            try:
                if move:
                    image_path.rename(target)
                    print(f" --> [OK] Moved {image_path} to {target}")
                else:
                    shutil.copyfile(image_path, target)
                    print(f" --> [OK] Copied {image_path} to {target}")
            except PermissionError as e:
                print(f"Permission Error: {e}")

def get_pictures_path(directory: Path) -> Set[Path]:
    """Return all png, jpg and jpeg firles in directory"""
    
    png_files = directory.rglob("*.[Pp][Nn][Gg]")
    jpg_files = directory.rglob("*.[Jj][Pp][Gg]")
    jpeg_files = directory.rglob("*.[Jj][Pp][Ee][Gg]")
    return set(png_files).union(jpg_files, jpeg_files)

def main():
    """Main function to process images."""
    argument = parse_arguments()
    source_directory = Path(argument.src_directory)
    check_directory(source_directory)
    if argument.debug:
        print("Source : " + str(source_directory))
    target_directory = Path(argument.target_directory)
    check_directory(target_directory, True)
    if argument.debug:
        print("Target : " + str(target_directory))
    paths = get_pictures_path(source_directory)
    if argument.debug:
        print("Paths : " + str(paths))
    nb_paths = len(paths)
    i = 0
    for path in paths:
        i = i+1
        print("[" + str(i) +"/"+ str(nb_paths)+"] Processing "+ str(path))
        process_image(path, target_directory, argument.move)

if __name__ == "__main__":
    main()
