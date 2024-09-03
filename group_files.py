import os
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from mutagen.flac import FLAC, FLACNoHeaderError

def list_files(directory):
    music_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3') or file.endswith('.flac'):
                music_files.append(os.path.join(root, file))
    return music_files

def show_metadata(file):
    try:
        if(file.endswith('.mp3')):
            audio = EasyID3(file)
        elif (file.endswith('.flac')):
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

def group_by_artist(files):
    artist_groups = {}
    for file in files:
        metadata = show_metadata(file)
        artist = metadata['Artist']
        if artist not in artist_groups:
            artist_groups[artist] = []
        artist_groups[artist].append(os.path.basename(file))
    return artist_groups

def group_by_album(files):
    album_groups = {}
    for file in files:
        metadata = show_metadata(file)
        album = metadata['Album']
        if album not in album_groups:
            album_groups[album] = []
        album_groups[album].append(os.path.basename(file))
    return album_groups

def group_by_artist_album(files):
    artist_album_groups = {}
    for file in files:
        metadata = show_metadata(file)
        artist = metadata['Artist']
        album = metadata['Album']
        if artist not in artist_album_groups:
            artist_album_groups[artist] = {}
        if album not in artist_album_groups[artist]:
            artist_album_groups[artist][album] = []
        artist_album_groups[artist][album].append(os.path.basename(file))
    return artist_album_groups

def print_grouped_data(grouped_data, depth=0):
    for group in sorted(grouped_data.keys()):
        data = grouped_data[group]
        print("│   " * depth + "├── " + group)
        if isinstance(data, dict):
            print_grouped_data(data, depth + 1)
        else:
            i = 0
            for i in range(len(sorted(data))-1):
                print("│   " * (depth + 1) + "│── " + data[i])
            print("│   " * (depth + 1) + "└── " + data[i])
            
            


def main():
    parser = argparse.ArgumentParser(description="Manage your Music Library")
    parser.add_argument('--input', type=str, required=True, help='Path to the music folder')
    parser.add_argument('--group-by', choices=['ARTIST', 'ALBUM', 'ARTIST_ALBUM'], required=True, help='Group music files by specified parameter')

    args = parser.parse_args()

    files = list_files(args.input)

    if args.group_by == 'ARTIST':
        grouped_data = group_by_artist(files)
    elif args.group_by == 'ALBUM':
        grouped_data = group_by_album(files)
    elif args.group_by == 'ARTIST_ALBUM':
        grouped_data = group_by_artist_album(files)
    print("Music")
    print_grouped_data(grouped_data)

if __name__ == '__main__':
    main()
