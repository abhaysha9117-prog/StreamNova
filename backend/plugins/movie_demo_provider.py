import requests
from bs4 import BeautifulSoup


class Plugin:

    name = "MovieDemo"

    BASE_URL = "https://test-streams.mux.dev"

    # ============================
    # SEARCH
    # ============================

    def search(self, query: str):

        print(f"🔍 Searching movie: {query}")

        return [

            {
                "title": f"{query} Movie Demo",
                "id": "demo-movie-1"
            }

        ]

    # ============================
    # GET EPISODES (Movies → Single item)
    # ============================

    def get_episodes(self, item_id: str):

        return [

            {
                "title": "Play Movie",
                "id": item_id
            }

        ]

    # ============================
    # GET STREAMS
    # ============================

    from extractors.html_extractor import HTMLExtractor


def get_streams(self, item_id: str):

    print(f"🎬 Extracting movie page")

    extractor = HTMLExtractor()

    # Demo HTML page

    test_page = "https://example.com"

    streams = extractor.extract(
        test_page
    )

    # fallback test stream

    if not streams:

        streams = [

            {
                "quality": "Auto",

                "url":
                "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
            }

        ]

    return {

        "streams": streams,

        "subtitles": []

    }