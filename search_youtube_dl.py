import os
import pandas as pd
from youtube import YouTube
import time

x = YouTube()

wd = '/Users/annie/github/music_text/'

if os.path.isfile(wd + 'to_youtube.csv'):
    os.remove(wd + 'to_youtube.csv')

its = 0
while True:
    print(its)
    its = its + 1
    time.sleep(2)
    if os.path.isfile(wd + 'to_youtube.csv'):
        to_youtube = pd.read_csv(wd + 'to_youtube.csv', header=None)
        to_youtube.columns = ['id', 'term']
    else:
        to_youtube = pd.DataFrame(columns=['id', 'term'])

    if os.path.isfile(wd + 'songs_found.csv'):
        songs_found = pd.read_csv(wd + 'songs_found.csv')
    else:
        songs_found = pd.DataFrame(
            columns=['id', 'term', 'vid_id', 'song_file'])
        songs_found.to_csv(wd + 'songs_found.csv', index = False)

    to_youtube = to_youtube[~to_youtube.id.isin(songs_found.id)]
    for index, row in to_youtube.iterrows():
        vid_id = x.find_video(row.term)
        if vid_id is not None:
            ydl = "youtube-dl -o '%s' -f 140 https://www.youtube.com/watch?v=%s"
            os.system(ydl % (wd + 'music/' + vid_id + '.%(ext)s', vid_id))
        else:
            vid_id = 'COULD_NOT_FIND'
        fd = open(wd + 'songs_found.csv', 'a')
        fd.write(','.join([row.id, row.term.encode('ascii', 'ignore'), vid_id, vid_id + '.m4a']))
        fd.write('\n')
        fd.close()
