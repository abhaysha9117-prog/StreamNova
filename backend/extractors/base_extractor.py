class BaseExtractor:

    name = "BaseExtractor"

    def extract(self, url: str):

        raise NotImplementedError(
            "Extractor must implement extract()"
        )