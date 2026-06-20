def get_streams(imdbID: str):

    print("Provider1:", imdbID)

    return [

        {
            "provider": "Provider 1",
            "quality": "480p",
            "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
        },

        {
            "provider": "Provider 1",
            "quality": "720p",
            "url": "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8"
        }

    ]