import os
import shutil
from datetime import datetime
from exif import Image
from pathlib import Path
from moviepy.editor import VideoFileClip
from PIL import Image as PILImage
import pillow_heif
import piexif

def get_date_taken(filepath):
    """Extract the date the image or video was taken."""
    try:
        if filepath.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            pass
            # with open(filepath, 'rb') as img_file:
            #     img = Image(img_file)
            #     if img.has_exif and hasattr(img, 'datetime_original'):
            #         return datetime.strptime(img.datetime_original, '%Y:%m:%d %H:%M:%S')
        elif filepath.suffix.lower() == '.heic':
            heif_image = pillow_heif.open_heif(filepath)
            exif_bytes = heif_image.info.get('exif', None)
            if exif_bytes:
                exif_data = piexif.load(exif_bytes)
                date_taken = exif_data['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
                if date_taken:
                    return datetime.strptime(date_taken.decode('utf-8'), '%Y:%m:%d %H:%M:%S')
        elif filepath.suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv']:
            pass
            # clip = VideoFileClip(str(filepath))
            # if clip.creation_date:
            #     return datetime.strptime(clip.creation_date, '%Y-%m-%dT%H:%M:%S')
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    return None


def organize_files_by_date(source_folder, destination_folder, move_files):
    """Organize files in the source folder into year/month folders based on metadata date."""
    source_folder = Path(source_folder)
    destination_folder = Path(destination_folder)
    log_file = destination_folder / "no_metadata_log.txt"
    duplicate_log_file = destination_folder / "duplicate_files_log.txt"

    with log_file.open('w') as log, duplicate_log_file.open('w') as duplicate_log:
        for root, _, files in os.walk(source_folder):
            for file in files:
                filepath = Path(root) / file
                date_taken = get_date_taken(filepath)

                if date_taken:
                    year_folder = destination_folder / str(date_taken.year)
                    month_folder = year_folder / f"{date_taken.month:02d}"
                    month_folder.mkdir(parents=True, exist_ok=True)

                    destination_path = month_folder / file
                    if destination_path.exists():
                        print(f"File already exists: {destination_path}. Logging.")
                        duplicate_log.write(f"{destination_path}\n")
                        continue

                    if move_files:
                        print(f"Moving {filepath} to {destination_path}")
                        shutil.move(str(filepath), destination_path)

                        # Check for corresponding .AAE file and move it
                        aae_file = filepath.with_suffix('.AAE')
                        if aae_file.exists():
                            aae_destination = month_folder / aae_file.name
                            print(f"Moving associated AAE file {aae_file} to {aae_destination}")
                            shutil.move(str(aae_file), aae_destination)
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
    4. Logs duplicate files into 'duplicate_files_log.txt' in the destination folder.
    5. Moves associated .AAE files if the original file is moved.
    
    Requirements:
    - Ensure the required libraries (exif, moviepy, pillow, pillow-heif, piexif) are installed.
    """
    import sys
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python script.py <source_folder> <destination_folder> [--move]")
        sys.exit(1)

    source = sys.argv[1]
    destination = sys.argv[2]
    move_files = len(sys.argv) == 4 and sys.argv[3] == "--move"

    organize_files_by_date(source, destination, move_files)

    print("Organizing complete! Check 'no_metadata_log.txt' for files without metadata and 'duplicate_files_log.txt' for duplicate files in the destination folder.")
