import logging
from abc import ABC, abstractmethod
from typing import Any, Tuple

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentLoader(ABC):
    @abstractmethod
    def load(self) -> Any:
        """
        Abstract method to load content.
        """
        raise NotImplementedError("Subclasses must implement this method")


class ContentLoadException(Exception):
    pass


class QuoteLoader(ContentLoader):
    def __init__(self, quote_url: str):
        """
        Initializes the QuoteLoader with a URL.
        :param quote_url: The URL to fetch the quote from.
        """
        self.quote_url = quote_url

    def load(self) -> Tuple[str, str]:
        """
        Loads a quote from the URL.
        :return: A tuple containing the quote and the author.
        :raises ContentLoadError: If there is an error loading the quote.
        """
        try:
            response = requests.get(self.quote_url)
            response.raise_for_status()
            data = response.json()
            quote = data.get("content")
            author = data.get("author")
            if quote is None or author is None:
                raise ContentLoadException("Incomplete data received.")
            logger.info("Successfully loaded quote.")
            return quote, author
        except requests.RequestException as e:
            logger.error(f"Error loading quote: {e}")
            raise ContentLoadException(f"Error loading quote: {e}")
        except ValueError as e:
            logger.error(f"Error parsing JSON response: {e}")
            raise ContentLoadException(f"Error parsing JSON response: {e}")


class ImageLoader(ContentLoader):
    def __init__(self, image_url: str):
        """
        Initializes the ImageLoader with a URL.
        :param image_url: The URL to fetch the image from.
        """
        self.image_url = image_url

    def load(self) -> str:
        """
        Loads an image URL.
        :return: The URL of the image.
        :raises ContentLoadError: If there is an error loading the image URL.
        """
        try:
            response = requests.get(self.image_url)
            response.raise_for_status()
            image_url = response.url
            logger.info("Successfully loaded image URL.")
            return image_url
        except requests.RequestException as e:
            logger.error(f"Error loading image URL: {e}")
            raise ContentLoadException(f"Error loading image URL: {e}")
