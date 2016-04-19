import pyglet
import pandas as pd
import time
import os
# http://pyglet.readthedocs.org/en/latest/programming_guide/media.html

if os.path.isfile('/Users/annie/github/music_text/' + 'songs_found.csv'):
	os.remove('/Users/annie/github/music_text/' + 'songs_found.csv')
# Create default song list
f = '/Users/annie/github/music_text/music/'
#songs = ['cheek.mp3', 'mack_knife.mp3', 'phantom.mp3']
songs = ['cheek.mp3']
sources = [pyglet.media.load(f + x) for x in songs]

player = pyglet.media.Player()

for s in sources:
	player.queue(s)

player.play()

songs_added_name = []
songs_added_id = []
its = 0

while True:

	print(its)
	its = its + 1
	time.sleep(2)

	if os.path.isfile('/Users/annie/github/music_text/' + 'songs_found.csv'):
		df = pd.read_csv('/Users/annie/github/music_text/' + 'songs_found.csv')
	else:
		df = pd.DataFrame(columns = ['id','term','vid_id','song_file'])
	df = df[~df.id.isin(songs_added_id)]

	for index, row in df.iterrows():
		print(row)
		songs_added_id.append(row.id)
		if row.song_file == 'NEXT':

			player.next_source()

			print('next')
		elif row.song_file != 'COULD_NOT_FIND.m4a':
			print(row.song_file)
			player.queue(pyglet.media.load(f + row.song_file))
			songs_added_name.append(row.song_file)

	if not player.playing:
		sources = [pyglet.media.load(f + x) for x in songs]
		for s in sources:
			player.queue(s)
		player.play()