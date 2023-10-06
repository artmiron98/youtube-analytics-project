import os
from googleapiclient.discovery import build

class Video():
    """Класс для ютуб-видео"""
    api_key: str = os.getenv('YouTube_API')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)




    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.video_id
                                           ).execute()
        self.video_title = self.video_response['items'][0]['snippet']['title']
        self.video_url = f'https://youtu.be/{self.video_id}'
        self.view_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        self.comment_count = self.video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id


    def __str__(self):
        return self.video_title




