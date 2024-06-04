import logging

from content_loader import QuoteLoader, ImageLoader, ContentLoadError
from teams_notifier import TeamsNotifier
import credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Main function to send a daily quote with an image to Teams.
    """
    quote_loader = QuoteLoader(credentials.QUOTES_URL)
    image_loader = ImageLoader(credentials.IMAGE_URL)
    notifier = TeamsNotifier(credentials.WEBHOOK_URL)

    try:
        quote, author = quote_loader.load()
        image_url = image_loader.load()
        notifier.send_quote_with_image(quote, author, image_url)
    except ContentLoadError as e:
        logger.error(f"Error in loading quote and image: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
