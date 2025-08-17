import os
import random

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
# YouTube APIの認証情報を設定
api_key = os.getenv('YOUTUBE_DATA_APIKEY', ' ')
if not api_key:
    raise ValueError("YouTube API key is not set. Please set the YOUTUBE_DATA_APIKEY environment variable.")

youtube = build('youtube', 'v3', developerKey=api_key)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}


class Fetch_Youtube_Links:
    """YouTubeリンクを取得するクラス"""

    def __init__(self, headers=headers):
        """初期化メソッド"""
        self.headers = headers

    def search_youtube_video(self, query, max_results):
        request = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=max_results,
            type='video'
        )
        response = request.execute()
        links = []
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            links.append(f"https://www.youtube.com/watch?v={video_id}")

        random_link = random.choice(links) if links else None
        return random_link

    def main(self, query, max_results):
        """メイン処理"""
        youtube_link = self.search_youtube_video(query, max_results)
        if youtube_link:
            print(f"こちらの動画が当たりました! \n {youtube_link}")
        else:
           print("No YouTube link found.")
        return youtube_link


if __name__ == "__main__":
    query = "大西葵ニアジョイ切り抜き"
    link = Fetch_Youtube_Links().main(query, max_results=100)