from extractors.extractor_manager import ExtractorManager


class Plugin:

    name = "MovieReal"

    # ============================
    # SEARCH
    # ============================

    def search(self, query: str):

        print(f"🔍 MovieReal searching: {query}")

        # Temporary fake search
        return [

            {
                "title": f"{query} Movie",
                "id": f"{query}-movie"
            }

        ]

    # ============================
    # GET EPISODES
    # ============================

    def get_episodes(self, item_id: str):

        # Movies = single play item

        return [

            {
                "title": "▶ Play Movie",
                "id": item_id
            }

        ]

    # ============================
    # GET STREAMS
    # ============================

    def get_streams(self, item_id: str):

        print("🎬 MovieReal extracting from page")

        manager = ExtractorManager()

        # Try extracting from page
        page_url = "https://example.com"

        streams = manager.extract(page_url)

        # Fallback if no streams found

        if not streams:

            print("⚠️ No streams found — using fallback")

            streams = manager.extract(
                "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
            )

        return {

            "streams": streams,

            "subtitles": [

                {
                    "label": "English",
                    "url":
                    "https://test-streams.mux.dev/x36xhzz/english.vtt"
                }

            ]

        }