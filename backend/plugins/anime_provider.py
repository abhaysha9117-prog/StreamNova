class Plugin:

    name = "AnimeReal"

    # ============================
    # SEARCH
    # ============================

    def search(self, query: str):

        print(f"🔍 Searching anime: {query}")

        return [

            {
                "title": f"{query} Season 1",
                "id": "naruto-season-1"
            }

        ]

    # ============================
    # GET EPISODES
    # ============================

    def get_episodes(self, item_id: str):

        print(f"📺 Getting episodes for: {item_id}")

        episodes = []

        for i in range(1, 6):

            episodes.append({

                "title": f"Episode {i}",

                "episode": i,

                "id": f"{item_id}-ep-{i}"

            })

        return episodes

    # ============================
    # GET STREAMS
    # ============================

    def get_streams(self, item_id: str):

        print(f"🎬 Getting streams for: {item_id}")

        return {

            "streams": [

                {
                    "quality": "720p",

                    "url":
                    "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
                }

            ],

            "subtitles": [

                {
                    "label": "English",

                    "url":
                    "https://test-streams.mux.dev/x36xhzz/english.vtt"
                }

            ]

        }