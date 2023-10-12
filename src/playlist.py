import os
from googleapiclient.discovery import build
import isodate
import datetime
from collections import OrderedDict
from operator import getitem
class PlayList():
    """Класс для ютуб-плэйлист"""
    api_key: str = os.getenv('YouTube_API')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    """Экземпляр инициализируется id плэйлиста. Дальше все данные будут подтягиваться по API."""
    def __init__(self, pl_id):
        self.pl_id = pl_id
        self.playlist_videos_time = PlayList.youtube.playlistItems().list(playlistId=self.pl_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        self.playlist_videos = PlayList.youtube.playlists().list(id=self.pl_id, part='snippet,contentDetails', maxResults=100).execute()
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos_time['items']]
        self.video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.video_ids)
                                               ).execute()
        self.url = f"https://www.youtube.com/playlist?list={self.pl_id}"
        self.title = self.playlist_videos['items'][0]['snippet']['title']

    """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""
    @property
    def total_duration(self):
        self.iso_8601_duration = isodate.parse_duration(self.video_response['items'][0]['contentDetails']['duration'])
        for video in self.video_response['items'][1:]:
            # YouTube video duration is in ISO 8601 format
            v_duration = video['contentDetails']['duration']
            self.iso_8601_duration += isodate.parse_duration(v_duration)
        return self.iso_8601_duration

    """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
    def show_best_video(self):
        #self.top_video = sorted(self.video_response, key=lambda x: int(self.video_response[x]['likeCount']))
        likes = 0
        self.url = ''
        for i in self.video_response['items']:
            if int(i['statistics']['likeCount']) > likes:
                likes = int(i['statistics']['likeCount'])
                self.url = i['id']
        return f'https://youtu.be/{self.url}'


