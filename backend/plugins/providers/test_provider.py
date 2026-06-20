def get_streams(movie_id: str):

    print("🎬 Provider called with:", movie_id)

    streams = [
        {
            "title": "Demo Stream 480p",
            "quality": "480p",
            "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
            "type": "hls"
        },

        {
            "title": "Demo Stream 720p",
            "quality": "720p",
            "url": "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8",
            "type": "hls"
        },

        {
            "title": "Demo Stream 1080p",
            "quality": "1080p",
            "url": "https://test-streams.mux.dev/test_001/stream.m3u8",
            "type": "hls"
        }
    ]

    return streams