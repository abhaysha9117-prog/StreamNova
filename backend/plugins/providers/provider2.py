def get_streams(imdbID: str):

    print("Provider2:", imdbID)

    return [

        {
            "provider": "Provider 2",
            "quality": "720p",
            "url": "https://test-streams.mux.dev/test_001/stream.m3u8"
        },

        {
            "provider": "Provider 2",
            "quality": "1080p",
            "url": "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8"
        }

    ]