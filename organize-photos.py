#!/usr/bin/env python3

import shutil
import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import argparse
import pillow_heif

pillow_heif.register_heif_opener()

MEDIA_EXTENSIONS = [
  "jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "heic",
  "mp4", "avi", "mov", "mkv", "webm", "flv", "wmv"
]

# Loops through all images in a directory and looks at the metadata to determine what
# year the image is from. Then moves the image to that year's folder. The file is also
# renamed to whatever the creation/modification timestamp of the image is
# Example of final path: IMG.jpg -> 2025/2025-09-07 03-36-43.jpg
def organize_images_by_year(dir_path):
  total = 0
  directory = os.fsencode(dir_path)

  for file in os.listdir(directory):
    file_name = file.decode("utf-8")
    file_extension = file_name.split('.')[-1]
    file_path = f'{dir_path}/{file_name}'

    if os.path.isdir(file_path) or file_extension.lower() not in MEDIA_EXTENSIONS:
      continue

    date = get_date_from_metadata(file_path)
    year = date[0:4]

    year_dir = f'{dir_path}/{year}'
    if not os.path.exists(year_dir):
      os.makedirs(year_dir)

    final_dst = handle_path_collision(year_dir, date, file_extension)

    shutil.move(file_path, final_dst)
    total += 1

  print('Images organized:', total)


# Looks for the DateTime exif field. If it doesn't exist or theres an error
# it returns the file modification date instead. Formatted as Y-m-d H-M-S
def get_date_from_metadata(img_path: str):
  try:
    img = Image.open(img_path)
    exif_data = img.getexif()

    if not exif_data:
      return get_modified_date(img_path)

    exif = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
    date_str = exif.get('DateTimeOriginal') or exif.get('CreateDate') or exif.get('DateTime')

    if not date_str:
      return get_modified_date(img_path)
    
    return str(date_str).replace(':', '-')
  except:
    return get_modified_date(img_path)


def get_modified_date(img_path):
  modified_time = os.path.getmtime(img_path)
  return datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H-%M-%S')


# If the file already exists, it will take the name of format Y-m-d H-M-S and
# add 1 to the last digit (the seconds)
def handle_path_collision(dir_path, name, file_extension):
  name_until_last_num = "-".join(name.split('-')[0:len(name.split('-'))-1])
  end_num = name.split('-')[-1]

  new_file_path = f'{dir_path}/{name_until_last_num}-{end_num}.{file_extension}'
  n = int(end_num)
  while os.path.exists(new_file_path):
    new_end_num = str(n).zfill(2)
    new_file_path = f'{dir_path}/{name_until_last_num}-{str(new_end_num)}.{file_extension}'
    n += 1

  return new_file_path


def parse_dir_path():
    parser = argparse.ArgumentParser(description="Parse a directory path.")
    parser.add_argument("path", type=str, help="Path to the directory")

    args = parser.parse_args()
    dir_path = args.path

    if not os.path.isdir(dir_path):
        print(f"Error: {dir_path} is not a valid path")
        exit(1)

    return dir_path


organize_images_by_year(parse_dir_path())