import json

import requests
from bs4 import BeautifulSoup

# BeatportのテクノチャートのURL
# URLは変更される可能性があるため、適宜確認してください
URL = "https://www.beatport.com/genre/uk-garage-bassline/86/top-100"

# Webサイトにアクセスするためのヘッダー情報
# これにより、プログラムからのアクセスをブラウザからのアクセスに見せかけます
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    # URLからHTMLコンテンツを取得
    response = requests.get(URL, headers=headers)
    response.raise_for_status()  # エラーがあれば例外を発生させる

    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(response.text, "html.parser")

    # ページのscriptタグからデータを取得
    # BeatportはページデータをJSON形式でscriptタグ内に埋め込んでいます
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})

    if not script_tag:
        print(
            "エラー: データが見つかりませんでした。サイトの構造が変更された可能性があります。"
        )
    else:
        # JSONデータをPythonの辞書型に変換
        data = json.loads(script_tag.string)

        # チャートのトラックリストを取得
        tracks = data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"][
            "data"
        ]["results"]

        print("🎧 Beatport Techno (Peak Time / Driving) Top 10 🎧")
        print("-" * 50)

        # 上位10曲をループで処理
        for i, track in enumerate(tracks[:10]):
            rank = i + 1
            # アーティスト名を取得（複数の場合は連結）
            artist_names = ", ".join([artist["name"] for artist in track["artists"]])
            track_name = track["name"]

            print(f"{rank:2d}. {track_name}")
            print(f"   👤 Artist: {artist_names}\n")

except requests.exceptions.RequestException as e:
    print(f"エラー: サイトにアクセスできませんでした。 - {e}")
except (KeyError, IndexError) as e:
    print(
        f"エラー: ページのデータ構造の解析に失敗しました。サイトが更新された可能性があります。 - {e}"
    )
