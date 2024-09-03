import os
import argparse
import requests
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
def search_music_metadata(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    url = 'https://musicbrainz.org/ws/2/recording'
    params = {
        'query': file_name,
        'fmt': 'json',
        'limit': 3  
    }
    
    response = requests.get(url, params=params)
    results = response.json().get('recordings', [])
    
    return results

def suggest_metadata_matches(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.mp3') or file.endswith('.flac'):
                file_path = os.path.join(root, file)
                matches = search_music_metadata(file_path)
                print(f'File: {file_path}')
                
                print('Top 3 matches:')
                for i, match in enumerate(matches[:3], start=1):
                    print(f"{i}. Song: {match.get('title', 'Unknown')}")
                    if 'releases' in match and match['releases']:
                        album = match['releases'][0].get('title', 'Unknown')
                    else:
                        album = 'Unknown'
                    print(f"   Album: {album}")
                    print(f"   Artist: {', '.join(artist.get('name', 'Unknown') for artist in match.get('artist-credit', []))}")
                print('---')
                yield file_path, matches

def update_metadata(file_path, choice):
    matches = list(suggest_metadata_matches(os.path.dirname(file_path)))
    match = matches[int(choice) - 1]
    new_metadata = match[1][int(choice) - 1]

    if(file_path.endswith('.mp3')):
        audio = EasyID3(file_path)
    elif(file_path.endswith('.flac')):
        audio = FLAC(file_path)
    
    # Updating metadata
    audio['title'] = new_metadata.get('title', [''])[0]
    audio['album'] = new_metadata.get('release', {}).get('title', ['Unknown'])[0]
    audio['artist'] = ', '.join(artist.get('name', 'Unknown') for artist in new_metadata.get('artist-credit', []))
    audio.save()

    print("Metadata updated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Music Metadata Suggestion Tool')
    parser.add_argument('--input', help='Path to the music folder', required=True)
    parser.add_argument('--update-metadata', action='store_true', help='Update metadata for music files')
    args = parser.parse_args()
    
    if args.update_metadata:
        for file_path, matches in suggest_metadata_matches(args.input):
            print(f"Do you wish to update {file_path}? (Y/N)")
            choice = input().strip().upper()
            if choice == "Y":
                print("Select correct choice (1, 2, 3):")
                update_choice = input().strip()
                update_metadata(file_path, update_choice)
            else:
                print("Metadata not updated.")
                print("---")
