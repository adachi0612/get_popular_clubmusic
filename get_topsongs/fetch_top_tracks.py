import json
import os
import sys

import requests
from bs4 import BeautifulSoup

# Windowsでの文字エンコーディング問題を解決
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"


headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}


class Fetch_Topsong:

    def __init__(self, url, headers=headers):
        """初期化メソッド"""
        self.url = url
        self.headers = headers

    def fetch_html(self):
        """指定URLからHTMLを取得する"""
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def extract_json_data(self, html):
        """HTMLからBeatportの埋め込みJSONデータを抽出する"""
        soup = BeautifulSoup(html, "html.parser")
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})

        if not script_tag:
            raise ValueError("エラー: データが見つかりませんでした。サイトの構造が変更された可能性があります。")
        json_str = script_tag.get_text()

        if not json_str:
            raise ValueError("エラー: JSONデータが空です。サイトの構造が変更された可能性があります。")
        return json.loads(json_str)

    def get_tracks_from_json(self, data):
        """JSONデータからトラックリストを取得する"""
        return data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["results"]

    def safe_print(self, text):
        """エンコーディングエラーを回避する安全な出力メソッド"""
        try:
            print(text)
        except UnicodeEncodeError:
            # エンコーディングエラーが発生した場合、ASCII文字のみで出力
            print(text.encode('ascii', 'ignore').decode('ascii'))

    def print_top_tracks(self, tracks, top_n=10):
        """上位N曲の情報を表示する"""
        track_names = []  # 曲名を保持するリスト
        artist_names_list = []  # アーティスト名を保持するリスト

        for track in tracks[:top_n]:
            artist_names = ", ".join([artist["name"] for artist in track["artists"]])
            track_name = track["name"]

            # リストに追加
            track_names.append(track_name)
            artist_names_list.append(artist_names)

        return track_names, artist_names_list

    def main(self):
        try:
            html = self.fetch_html()
            data = self.extract_json_data(html)
            tracks = self.get_tracks_from_json(data)
            track_names, artist_names_list = self.print_top_tracks(tracks, top_n=10)

            # リストを返すことも可能
            return track_names, artist_names_list

        except requests.exceptions.RequestException as e:
            self.safe_print(f"エラー: サイトにアクセスできませんでした。 - {e}")

        except (KeyError, IndexError, ValueError) as e:
            self.safe_print(f"エラー: ページのデータ構造の解析に失敗しました。サイトが更新された可能性があります。 - {e}")
