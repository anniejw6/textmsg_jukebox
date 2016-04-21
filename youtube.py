import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import pandas as pd
import re

import isodate

from auth import CLIENT_SECRETS_FILE, DEVELOPER_KEY


class YouTube(object):

    def __init__(self, playlist='', developer_key = DEVELOPER_KEY):
        self.youtube = self.authenticate(developer_key)
        self.playlist = playlist

    def authenticate(self, developer_key):
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=developer_key)
        
        return(youtube)

    # def create_playlist(self, title_text, description_text,
    # 	privacy = 'unlisted'):
    # 	response = self.youtube.playlists().insert(
    # 		part = "snippet, status",
    # 		body = dict(
    # 			snippet = dict(
    # 				title = title_text,
    # 				description = description_text
    # 				),
    # 			status = dict(
    # 				privacyStatus = privacy
    # 				)
    # 			)
    # 		).execute()
    # 	print('Created new playlist: %s' % response['id'])
    # 	return(response)

    # def add_video(self, playlist, video_id):
    # 	response = self.youtube.playlistItems().insert(
    # 		part="snippet",
    # 		body=dict(
    # 			snippet=dict(
    # 				playlistId= playlist,
    # 				resourceId=dict(
    # 					kind="youtube#video",
    # 					videoId= video_id
    # 					)
    # 				)
    # 			)
    # 		).execute()
    # 	print('Added new video')
    # 	return(response)

    def find_video(self, search_term,
                   max_results=5, max_duration=420):
        # Find all list of video
        y = self._search_video(search_term, max_results)
        vid = [vids['id']['videoId'] for vids in y['items']]
        # Validate the duration and return first
        valid = [self._video_limit(v) for v in vid]
        first_valid = valid.index(True) if True in valid else None
        if first_valid is not None:
            return(vid[first_valid])
        else:
            print('No valid videos found')

    def _search_video(self, search_term,
                      max_results=5):
        response = self.youtube.search().list(
            q=search_term,
            part="id,snippet",
            maxResults=max_results,
            type="video"
        ).execute()
        return(response)

    def _video_limit(self, video_id,
                     max_duration=420):
        response = self.youtube.videos().list(
            id=video_id,
            part="contentDetails,id"
        ).execute()
        try: 
            duration = response['items'][0]['contentDetails']['duration']
            duration = isodate.parse_duration(duration).total_seconds()
        except:
            duration = float("inf")
        return(duration <= max_duration)


if __name__ == '__main__':
    x = YouTube()
    print(x.find_video('hello kitty'))
    print(x.youtube)
    print('success')
