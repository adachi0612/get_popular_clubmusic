# fetch_top_tracks.pyからFetch_Topsongクラスをインポート
from fetch_youtube_links import Fetch_Youtube_Links

URL = "https://www.beatport.com/genre/uk-garage-bassline/86/top-100"

fetcher = Fetch_Youtube_Links(URL).main()