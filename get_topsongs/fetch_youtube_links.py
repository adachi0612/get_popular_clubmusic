import os

from dotenv import load_dotenv
from fetch_top_tracks import Fetch_Topsong, headers
from googleapiclient.discovery import build

load_dotenv()
# YouTube APIの認証情報を設定
api_key = os.getenv('YOUTUBE_DATA_APIKEY', ' ')
if not api_key:
    raise ValueError("YouTube API key is not set. Please set the YOUTUBE_DATA_APIKEY environment variable.")
youtube = build('youtube', 'v3', developerKey=api_key)


class Fetch_Youtube_Links:
    """YouTubeリンクを取得するクラス"""
    def __init__(self, URL, headers=headers):
        self.url = URL
        self.headers = headers

    def make_youtube_query(self, artist_name, track_name):
        """YouTube検索用クエリを生成"""
        return f"{artist_name} - {track_name} official audio"

    def search_youtube_video(self, query):
        request = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=1,
            type='video'
        )
        response = request.execute()
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
        return None

    def main(self):
        fetcher = Fetch_Topsong(self.url, self.headers)
        result = fetcher.main()
        if result is None:
            print("曲リストの取得に失敗しました。")
            return
        track_names, artist_names_list = result

        for track_name, artist_name in zip(track_names, artist_names_list):
            query = self.make_youtube_query(artist_name, track_name)
            youtube_link = self.search_youtube_video(query)
            print(f"{track_name} / {artist_name}")
            if youtube_link:
                print(youtube_link)
            else:
                print("No video found.")
            print("-" * 40)