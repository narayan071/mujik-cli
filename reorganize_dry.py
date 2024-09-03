import os
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.flac import FLACNoHeaderError, FLAC
from group_files import list_files
# def list_files(directory):
#     music_files = []
#     for root, _, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.mp3') or file.endswith('.flac'):
#                 music_files.append(os.path.join(root, file))
#     return music_files

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

def dry_run_reorganize_by_artist(files):
    changes = {}
    for file in files:
        metadata = show_metadata(file)
        artist = metadata['Artist']
        source_path = file
        destination_path = os.path.join(os.path.dirname(file), artist, os.path.basename(file))
        if source_path != destination_path:
            changes[source_path] = destination_path
    return changes

def dry_run_reorganize_by_album(files):
    changes = {}
    for file in files:
        metadata = show_metadata(file)
        album = metadata['Album']
        source_path = file
        destination_path = os.path.join(os.path.dirname(file), album, os.path.basename(file))
        if source_path != destination_path:
            changes[source_path] = destination_path
    return changes

def dry_run_reorganize_by_artist_album(files):
    changes = {}
    for file in files:
        metadata = show_metadata(file)
        artist = metadata['Artist']
        album = metadata['Album']
        source_path = file
        destination_path = os.path.join(os.path.dirname(file), artist, album, os.path.basename(file))
        if source_path != destination_path:
            changes[source_path] = destination_path
    return changes

def main():
    parser = argparse.ArgumentParser(description="Manage your Music Library")
    parser.add_argument('--input', type=str, required=True, help='Path to the music folder')
    parser.add_argument('--reorganize-by', choices=['ARTIST', 'ALBUM', 'ARTIST_ALBUM'], required=True, help='Reorganize music files by specified parameter')
    parser.add_argument('--dry-run', action='store_true', help='Perform dry run (list changes without moving files)')

    args = parser.parse_args()

    files = list_files(args.input)

    if args.reorganize_by == 'ARTIST':
        changes = dry_run_reorganize_by_artist(files)
    elif args.reorganize_by == 'ALBUM':
        changes = dry_run_reorganize_by_album(files)
    elif args.reorganize_by == 'ARTIST_ALBUM':
        changes = dry_run_reorganize_by_artist_album(files)

    if args.dry_run:
        print("The following changes will be made to your library:")
        for source, destination in changes.items():
            print(f"Moved {source} ---> {destination}")

if __name__ == '__main__':
    main()
