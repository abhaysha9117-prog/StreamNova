import requests
from bs4 import BeautifulSoup

from extractors.base_extractor import BaseExtractor


class IframeExtractor(BaseExtractor):

    name = "IframeExtractor"

    def extract(self, url: str):

        print(f"🌐 Loading page: {url}")

        streams = []

        try:

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            r = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            soup = BeautifulSoup(
                r.text,
                "html.parser"
            )

            # Find iframe

            iframe = soup.find("iframe")

            if iframe:

                iframe_url = iframe.get("src")

                print(
                    f"📺 Found iframe: {iframe_url}"
                )

                streams.append({

                    "quality": "Auto",
                    "url": iframe_url

                })

        except Exception as e:

            print("Iframe extractor error:", e)

        return streams