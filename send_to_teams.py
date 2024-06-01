import requests
import logging

from PIL import Image
from io import BytesIO

from content_loader import ContentLoader
import credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TeamsNotifier:
    def __init__(self, quote_loader: ContentLoader, image_loader: ContentLoader):
        self.quote_loader = quote_loader
        self.image_loader = image_loader
        self.webhook_url = credentials.WEBHOOK_URL

    def action(self):
        quote, author = self.quote_loader.load()
        image_url = self.image_loader.load()

        if not image_url:
            logger.error("Error loading image")
            return

        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image.show()
            logger.info("Image displayed successfully.")
            print(f"Quote: {quote}")
            print(f"Quote: {author}")
        except requests.RequestException as e:
            logger.error(f"Error displaying image: {e}")

        self._send_to_teams(image_url, quote, author)

    def _send_to_teams(self, image_url, quote, author):
        message_data = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.2",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": "Daily Quote - By Nikoloz Aneli",
                                "size": "Large",
                                "weight": "Bolder"
                            },
                            {
                                "type": "TextBlock",
                                "text": quote,
                                "wrap": True
                            },
                            {
                                "type": "TextBlock",
                                "text": f"-{author}",
                                "wrap": True,
                                "size": "Medium",
                                "spacing": "Medium"
                            },
                            {
                                "type": "Image",
                                "url": image_url,
                                "size": "Stretch"
                            }
                        ]
                    }
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(self.webhook_url, headers=headers, json=message_data)
            response.raise_for_status()
            logger.info(f"Message sent successfully. Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
        except requests.RequestException as e:
            logger.error(f"Error sending message to Teams: {e}")
