import json
import os

from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YouTube_API')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    @property
    def channel_id(self):
        return self.__channel_id

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriberCount = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other):
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __lt__(self, other):
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def __eq__(self, other):
        return int(self.subscriberCount) == int(other.subscriberCount)



    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute())

    @classmethod
    def get_service(cls):
        """Возвращающает объект для работы с YouTube API"""
        api_key: str = os.getenv('YouTube_API')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""
        self.file = file
        arrt_values = {'channel_id': self.__channel_id,
                       'title': self.title,
                       'description': self.description,
                       'url': self.url,
                       'subscriberCount': self.subscriberCount,
                       'video_count': self.video_count,
                       'viewCount': self.viewCount}
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(arrt_values, f, indent = 2, ensure_ascii = False)
        