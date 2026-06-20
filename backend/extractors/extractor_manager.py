from extractors.m3u8_extractor import M3U8Extractor
from extractors.html_extractor import HTMLExtractor
from extractors.iframe_extractor import IframeExtractor


class ExtractorManager:

    def __init__(self):

        self.m3u8 = M3U8Extractor()
        self.html = HTMLExtractor()
        self.iframe = IframeExtractor()

    def extract(self, url: str):

        print(f"🔍 Selecting extractor for: {url}")

        try:

            # Direct stream

            if ".m3u8" in url:

                print("🎬 Using M3U8 extractor")

                return self.m3u8.extract(url)

            # Try iframe first

            print("📺 Trying iframe extractor")

            streams = self.iframe.extract(url)

            if streams:

                return streams

            # Fallback HTML

            print("🌐 Using HTML extractor")

            return self.html.extract(url)

        except Exception as e:

            print("❌ Extractor error:", e)

            return []