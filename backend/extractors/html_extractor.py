import requests
from bs4 import BeautifulSoup

from extractors.base_extractor import BaseExtractor


class HTMLExtractor(BaseExtractor):

    name = "HTMLExtractor"

    def extract(self, url: str):

        print(f"🌐 Extracting HTML: {url}")

        streams = []

        try:

            headers = {

                "User-Agent":
                "Mozilla/5.0"

            }

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Look for iframe
            iframe = soup.find("iframe")

            if iframe:

                iframe_src = iframe.get("src")

                print(
                    f"📺 Found iframe: {iframe_src}"
                )

                streams.append({

                    "quality": "Auto",

                    "url": iframe_src

                })

        except Exception as e:

            print(f"Extractor error: {e}")

        return streams