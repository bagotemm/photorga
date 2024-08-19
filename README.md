# Photo Organisator

This script copy/move picture files according to year/month of exif tag 'EXIF DateTimeOriginal' 

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
usage: photorga.py [-h] [-s SRC_DIRECTORY] [-t TARGET_DIRECTORY] [-m]

Move photos to directory with time of their creation

options:
  -h, --help            show this help message and exit
  -s SRC_DIRECTORY, --src_directory SRC_DIRECTORY
                        source directory
  -t TARGET_DIRECTORY, --target_directory TARGET_DIRECTORY
                        target directory
  -m, --move            Move insted of co
```

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0)