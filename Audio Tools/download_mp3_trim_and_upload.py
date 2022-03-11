import pandas as pd
import os
import urllib.request
import time as dur
from urllib.parse import urlparse
from tinytag import TinyTag
from pydub import AudioSegment
from fileUpload import uploadDrive
from pydub.utils import mediainfo

filepath = r"D:\ML\Musiio\PoCs\Roblox\seg_3.csv"

audio_link_list = []
segment_file_name = [] 
song_title = []
artist_name = []
#composer_name = []
segment_file_path = []
duration_delta = []
full_song_duration = []
musiio_track_id = []
preview_segment = []
preview_segment_score = []

source = pd.read_csv(filepath, header='infer')


def time_milliseconds(time):
    # Converts "M:S:MS" to milliseconds
    milliseconds = sum(x * int(t) for x, t in zip([60 * 1000, 1 * 1000, 1], time.split(":")))
    return milliseconds
   
for ind in source.index:
    # File download
    url = source['URL_FILENAME'][ind]
    split = urlparse(url)
    file_name = split.path.split("/")[-1]
    target_folder = 'D:/ML/Musiio/PoCs/Roblox/Segments_3/' ###location to save files and segments, ###add create directory, ###check buffer vs. saving
    target_file_path = target_folder + file_name + '.mp3'
    urllib.request.urlretrieve(url, target_file_path) 
    #file = file_orig.replace('file://', '')
       
    ###add functionality to flag links without duration and leave a note in the spreadsheet
      
    # Opening file and trimming down to a segment
    song = AudioSegment.from_file(target_file_path)
    
    # Add to list of original urls
    audio_link_list.append(url)
         
    # Segment selection
    segment_Time = source['PREVIEW SEGMENT 3'][ind]
    segment_Time_split = segment_Time.split('-')
    startTime = time_milliseconds(segment_Time_split[0])
    endTime = time_milliseconds(segment_Time_split[1])
    
    # Checks if segment is longer than full song and add full song duration
    duration_delta_value = (song.duration_seconds - (endTime / 1000))
    duration_delta.append(round(duration_delta_value, 3))
    song_duration = dur.strftime('%M:%S', dur.gmtime(song.duration_seconds))
    full_song_duration.append(song_duration)
    
    #if (song.duration_seconds * 1000) > endTime:
    extract = song[startTime:endTime]
        
    # Saving segment and creating a list of segment file names and file paths to use in dataframe when uploading to Drive
    segment_target_file_path = target_folder + file_name + '-segment_45_3.mp3'
    extract.export(segment_target_file_path, format="mp3", tags=mediainfo(target_file_path).get('TAG', {}))
    segment_file_path.append(segment_target_file_path)
    segment_file_name.append(file_name + '-segment_45_3.mp3')
                
    # Metadata extraction
    tag = TinyTag.get(target_file_path)
    song = tag.title
    artist = tag.artist
    artist_album = tag.albumartist
    #composer = tag.composer
                
    # Create metadata lists
    song_title.append(song)
    #artist_name.append(artist_album)
    if artist_album is None:
        artist_name.append(artist)
    else: artist_name.append(artist_album)   
    #composer_name.append(composer)
    
    # Add other columns from file
    musiio_track_id.append(source['MUSIIO TMP ID'][ind])
    preview_segment.append(segment_Time)
    preview_segment_score.append(source['SCORE'][ind])
    
    # Delete original file
    os.remove(target_file_path)
        
# Create dataframes            
drive_input = {'segment_path': segment_file_path, 'segment_file_name': segment_file_name}
original_url = {'ORIGINAL URL': audio_link_list, 'TITLE': song_title, 'ARTIST': artist_name,
                'name': segment_file_name, 'DURATION DELTA (s)': duration_delta, 'FULL SONG DURATION': full_song_duration,
                'MUSIIO TRACK ID': musiio_track_id, 'PREVIEW SEGMENT 1': preview_segment, 'SCORE': preview_segment_score}

drive_upload_list = pd.DataFrame(drive_input)
original_links = pd.DataFrame(original_url)

# Export original links and metadata
original_links.to_csv(path_or_buf=r"D:\ML\Musiio\PoCs\Roblox\Roblox_original_links_metadata_output.csv", sep=',', index=False, encoding='utf-8-sig')

folder_id = ''
target_file_path = r"D:\ML\Musiio\PoCs\Roblox\Roblox_output_mp3.csv"

# Upload to Drive
drive_df = uploadDrive(folder_id, drive_upload_list, target_file_path) ###check if drive folder empty to avoid duplication

# Dataframe merge
dataframe_join = pd.merge(original_links, 
                      drive_df, 
                      on ='name', 
                      how ='left')

# Reorder and add empty ISRC column
dataframe_join = dataframe_join.rename(columns={'webViewLink': 'URL'})
dataframe_join = dataframe_join[['ORIGINAL URL', 'URL', 'MUSIIO TRACK ID', 'TITLE', 'ARTIST', 'PREVIEW SEGMENT 3', 'SCORE','DURATION DELTA (s)', 'FULL SONG DURATION']]
dataframe_join.insert(loc=2, column='ISRC', value=None)

dataframe_join.to_csv(path_or_buf=r"D:\ML\Musiio\PoCs\Roblox\Roblox_output_mp3.csv", sep=',', index=False, encoding='utf-8-sig')