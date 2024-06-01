import requests
import logging
import credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentLoader:
    def load(self):
        raise NotImplementedError("Implement Subclasses")


class QuoteLoader(ContentLoader):
    def __init__(self):
        self.quote_url = credentials.QUOTES_URL

    def load(self):
        try:
            response = requests.get(self.quote_url)
            response.raise_for_status()
            quote = response.json()['content']
            author = response.json()['author']
            logger.info("Successfully loaded quote.")
            return quote, author
        except requests.RequestException as e:
            logger.error(f"Error loading quote: {e}")
            return "No quote found."


class ImageLoader(ContentLoader):
    def __init__(self):
        self.image_url = credentials.IMAGE_URL

    def load(self):
        try:
            response = requests.get(self.image_url)
            response.raise_for_status()
            image_url = response.url
            logger.info("Successfully loaded image URL.")
            return image_url
        except requests.RequestException as e:
            logger.error(f"Error loading image URL: {e}")
            return None
