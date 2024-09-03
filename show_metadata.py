#os to do file handling
import os
#argparse to parse the command in the command line
import argparse
#making use of mutagen package to extract metadata from the files
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC, FLACNoHeaderError
from mutagen.id3 import ID3NoHeaderError


def list_files(directory):
    music_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if (file.endswith('.mp3') or file.endswith('.flac')):
                music_files.append(os.path.join(root, file))
    return music_files

def show_metadata(file):
    try:
        if(file.endswith('.mp3')):
            audio = EasyID3(file)
        elif(file.endswith('.flac')):
            audio = FLAC(file)
        metadata = {
            'Song': audio.get('title', ['Unknown'])[0],
            'Artist': audio.get('artist', ['Unknown'])[0],
            'Album': audio.get('album', ['Unknown'])[0]
        }
    except (ID3NoHeaderError, FLACNoHeaderError):
        metadata = {
            'Song': 'Unknown',
            'Artist': 'Unknown',
            'Album': 'Unknown'
        }
    return metadata

def main():
    parser = argparse.ArgumentParser(description="Manage your Music Library")
    parser.add_argument('--input', type=str, required=True, help='Path to the music folder')
    parser.add_argument('--list-files', action='store_true', help='List all music files')
    parser.add_argument('--show-metadata', action='store_true', help='Show metadata for all music files')

    args = parser.parse_args()

    # needs the files to get metadata
    if args.show_metadata:
        files = list_files(args.input)
        for file in files:
            metadata = show_metadata(file)
            # filename, _ = os.path.splitext(file)
            print("____________________")
            print(f"File: {file}")
            print(f"Song: {metadata['Song']}")
            print(f"Artist: {metadata['Artist']}")
            print(f"Album: {metadata['Album']}")


if __name__ == '__main__':
    main()
