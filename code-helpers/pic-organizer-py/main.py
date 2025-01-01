import os
import shutil
from datetime import datetime
from exif import Image
from pathlib import Path
from moviepy.editor import VideoFileClip
import pyheif
from PIL import Image as PILImage

def get_date_taken(filepath):
    """Extract the date the image or video was taken."""
    try:
        if filepath.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            with open(filepath, 'rb') as img_file:
                img = Image(img_file)
                if img.has_exif and hasattr(img, 'datetime_original'):
                    return datetime.strptime(img.datetime_original, '%Y:%m:%d %H:%M:%S')
        elif filepath.suffix.lower() == '.heic':
            heif_file = pyheif.read(filepath)
            for metadata in heif_file.metadata or []:
                if metadata['type'] == 'Exif':
                    exif_data = PILImage.open(filepath)._getexif()
                    if exif_data:
                        date_taken = exif_data.get(36867)  # Tag for DateTimeOriginal
                        if date_taken:
                            return datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
        elif filepath.suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv']:
            clip = VideoFileClip(str(filepath))
            if clip.creation_date:
                return datetime.strptime(clip.creation_date, '%Y-%m-%dT%H:%M:%S')
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    return None


def organize_files_by_date(source_folder, destination_folder, move_files):
    """Organize files in the source folder into year/month folders based on metadata date."""
    source_folder = Path(source_folder)
    destination_folder = Path(destination_folder)
    log_file = destination_folder / "no_metadata_log.txt"

    with log_file.open('w') as log:
        for root, _, files in os.walk(source_folder):
            for file in files:
                filepath = Path(root) / file
                date_taken = get_date_taken(filepath)

                if date_taken:
                    year_folder = destination_folder / str(date_taken.year)
                    month_folder = year_folder / f"{date_taken.month:02d}"
                    month_folder.mkdir(parents=True, exist_ok=True)

                    destination_path = month_folder / file
                    if move_files:
                        print(f"Moving {filepath} to {destination_path}")
                        shutil.move(str(filepath), destination_path)
                    else:
                        print(f"Copying {filepath} to {destination_path}")
                        shutil.copy2(str(filepath), destination_path)
                else:
                    print(f"No metadata found for {filepath}. Logging.")
                    log.write(f"{filepath}\n")


if __name__ == "__main__":
    """
    This script organizes images and videos into folders based on their metadata 'date taken'.

    Usage:
    - Provide the source folder as the first argument.
    - Provide the destination folder as the second argument.
    - Optionally, use the "--move" flag as the third argument to move files instead of copying.

    The script:
    1. Reads the metadata of each file to determine the 'date taken'.
    2. Copies or moves the file into a folder structure organized by year and month.
    3. Logs files without metadata into 'no_metadata_log.txt' in the destination folder.
    
    Requirements:
    - Ensure the required libraries (exif, moviepy, pyheif, pillow) are installed.
    """
    import sys
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python script.py <source_folder> <destination_folder> [--move]")
        sys.exit(1)

    source = sys.argv[1]
    destination = sys.argv[2]
    move_files = len(sys.argv) == 4 and sys.argv[3] == "--move"

    organize_files_by_date(source, destination, move_files)

    print("Organizing complete! Check 'no_metadata_log.txt' in the destination folder for files without metadata.")
