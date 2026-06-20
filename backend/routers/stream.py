from fastapi import APIRouter

router = APIRouter()

@router.get("/stream")
def get_stream(
    imdbID: str,
    season: int = 1,
    episode: int = 1
):

    return {

        # 🎥 Video Streams
        "streams": [

            # AUTO (master playlist)
            {
                "quality": "Auto",
                "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
            },

            # Manual fallback qualities
            {
                "quality": "480p",
                "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
            },

            {
                "quality": "720p",
                "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
            },

            {
                "quality": "1080p",
                "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
            }

        ],

        # 📝 Subtitles
        "subtitles": [

            {
                "label": "English",
                "url": "https://test-streams.mux.dev/x36xhzz/english.vtt"
            },

            {
                "label": "Hindi",
                "url": "https://test-streams.mux.dev/x36xhzz/hindi.vtt"
            }

        ]

    }