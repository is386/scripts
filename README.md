# scripts

A collection of personal utility scripts.

## organize-photos.py

Organizes photos and videos in a directory by year based on their metadata. Files are moved into year-based subdirectories and renamed using their creation/modification timestamp.

**Before:**
```
photos/
  IMG_001.jpg
  IMG_002.heic
  video.mp4
```

**After:**
```
photos/
  2024/
    2024-09-07 03-36-43.jpg
    2024-11-20 14-22-01.heic
  2025/
    2025-01-15 08-10-30.mp4
```

### Usage

```bash
pip install -r requirements.txt
python organize-photos.py /path/to/photos
```

The script reads EXIF data to determine the original date. If no EXIF data is available, it falls back to the file's modification date.
