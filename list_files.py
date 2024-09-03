import os
import argparse

def list_files(directory):
    music_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3') or file.endswith('.flac'):
                music_files.append(file) 
    return music_files

def main():
    parser = argparse.ArgumentParser(description="List all MP3 files in the specified directory")
    parser.add_argument('--input', type=str, required=True, help='Path to the music folder')
    parser.add_argument('--list-files', action='store_true', help='List all music files')

    args = parser.parse_args()

    if args.list_files:
        files = list_files(args.input)
        for file in files:
            print(file)

if __name__ == '__main__':
    main()
