import os
import shutil
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.flac import FLAC, FLACNoHeaderError
from group_files import list_files
from show_metadata import show_metadata

def reorganize_files(files, group_by):
    for file in files:
        metadata = show_metadata(file)
        artist = metadata['Artist']
        album = metadata['Album']

        if group_by == 'ARTIST':
            destination = os.path.join(os.path.dirname(file), artist, os.path.basename(file))
        elif group_by == 'ALBUM':
            destination = os.path.join(os.path.dirname(file), album, os.path.basename(file))
        elif group_by == 'ARTIST_ALBUM':
            destination = os.path.join(os.path.dirname(file), artist, album, os.path.basename(file))

        print(f"Moved {file} ---> {destination}")
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.move(file, destination)

def main():
    parser = argparse.ArgumentParser(description="Manage your Music Library")
    parser.add_argument('--input', type=str, required=True, help='Path to the music folder')
    parser.add_argument('--reorganize-by', choices=['ARTIST', 'ALBUM', 'ARTIST_ALBUM'], required=True, help='Reorganize music files by specified parameter')

    args = parser.parse_args()

    files = list_files(args.input)

    reorganize_files(files, args.reorganize_by)

if __name__ == '__main__':
    main()
