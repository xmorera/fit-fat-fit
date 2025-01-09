from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def get_mov_creation_date(file_path):
    """
    Extract the creation date from a .mov file's metadata.

    Args:
        file_path (str): Path to the .mov file.

    Returns:
        str: The creation date of the file, or None if not found.
    """
    try:
        parser = createParser(file_path)
        if not parser:
            print(f"Unable to parse the file: {file_path}")
            return None

        metadata = extractMetadata(parser)
        if not metadata:
            print(f"No metadata found for the file: {file_path}")
            return None

        # Extract creation date
        creation_date = metadata.get("creation_date")
        if creation_date:
            return str(creation_date)
        else:
            print("Creation date not found in metadata.")
    except Exception as e:
        print(f"Error reading file metadata: {e}")
    return None

if __name__ == "__main__":
    file_path = "C:\\Data\\OneDrive\\Pictures\\Irene\\AALP2534.MOV"
    creation_date = get_mov_creation_date(file_path)
    if creation_date:
        print(f"Creation date of the file: {creation_date}")
    else:
        print("Creation date could not be extracted.")
