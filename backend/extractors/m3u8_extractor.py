import requests

from extractors.base_extractor import BaseExtractor


class M3U8Extractor(BaseExtractor):

    name = "M3U8Extractor"

    def extract(self, url: str):

        print(f"🎬 Extracting M3U8: {url}")

        streams = []

        try:

            # Simple test

            streams.append({

                "quality": "Auto",

                "url": url

            })

        except Exception as e:

            print(e)

        return streams