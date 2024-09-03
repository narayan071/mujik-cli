# Music Library Manager
(built using python)

## STEP 0: please install the required dependencies for the project using command
```shell
pip install -r requirements.txt
``` 
(make sure you're in the file location: ```\SURYA\silicon-2024-narayan071\music``` to be able to run the commands in command line)

The goal of this problem is to create a Music Library Manager in a STEP-by-STEP process, incrementally adding features.

## STEP 1: listing music file names stored in the Music library: 
#### use the following command to show the files
```shell
python list_files.py  --input Music --list-files
```

## STEP 2: showing metadata of music files using mutagen package: 
#### use the following command to show the metadata to each music file in the Music library: 

```shell
python show_metadata.py --input Music --show-metadata
```


## STEP 3: grouping files and showing in stdout

#### use the following to group by artist name

```shell
python group_files.py --input Music --group-by ARTIST
```

#### use the following to group by album name

```shell
python group_files.py --input Music --group-by ALBUM
```

#### use the following to group by album name and artist name

```shell
python group_files.py --input Music --group-by ARTIST_ALBUM
```

## STEP 4: dry running reorganizing/moving action by parameter

#### use the following to show dry run of reorganizing Music folder by artist

```shell
python reorganize_dry.py --input Music --reorganize-by ARTIST --dry-run
  
```
#### use the following to show dry run of reorganizing Music folder by album

```shell
python reorganize_dry.py --input Music --reorganize-by ALBUM --dry-run

```
#### use the following to show dry run of reorganizing Music folder by artist-album

```shell
python reorganize_dry.py --input Music --reorganize-by ARTIST_ALBUM --dry-run

```

## STEP 5: reorganizing/moving action by parameter

#### use the following to reorganize the Music folder by artists (artist -> music file)

```shell
python reorganize.py --input Music --reorganize-by ARTIST
```
#### use the following to reorganize the Music folder by albums(album->music file)

```shell
python reorganize.py --input Music --reorganize-by ALBUM
```
#### use the following to reorganize the Music folder by artist-album(artists->album->music file)

```shell
python reorganize.py --input Music --reorganize-by ARTIST
```


## STEP 6: Displaying Metadata from the Internet

#### use the following command to display metadata from the internet for music files in Music folder

```shell
python metadata_from_internet.py --input Music --suggest-metadata-matches
```

## STEP 7: Update metadata from suggested the internet

```shell
python update_metadata.py --input Music --update-metadata
```