import os
import argparse
import requests

def search_music_metadata(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    url = 'https://musicbrainz.org/ws/2/recording'
    params = {
        'query': file_name,
        'fmt': 'json',
        'limit': 3  
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status() 
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
                    title = match.get('title', 'Unknown')
                    artist_names = ', '.join(artist.get('name', 'Unknown') for artist in match.get('artist-credit', []))
                    
                    if 'releases' in match and match['releases']:
                        album = match['releases'][0].get('title', 'Unknown')
                    else:
                        album = 'Unknown'

                    print(f"{i}. Song: {title}")
                    print(f"   Album: {album}")
                    print(f"   Artist: {artist_names}")
                print('---')

def main():
    parser = argparse.ArgumentParser(description='Music Metadata Suggestion Tool')
    parser.add_argument('--input', help='Path to the music folder', required=True)
    parser.add_argument('--suggest-metadata-matches', action='store_true', help='Suggest metadata matches for music files')
    args = parser.parse_args()
    
    if args.suggest_metadata_matches:
        suggest_metadata_matches(args.input)

if __name__ == "__main__":
    main()
