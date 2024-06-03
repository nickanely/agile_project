import logging
import requests

from typing import Any, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    "Content-Type": "application/json",
}
 

class TeamsNotifier:
    def __init__(self, webhook_url: str):
        """
        Initializes the TeamsNotifier with a webhook URL.
        :param: webhook_url: The webhook URL for the Teams.
        """
        self.webhook_url = webhook_url

    def send_message(self, message: str) -> None:
        """
        Sends a plain text message to Teams.
        :param message: The message to send.
        """
        try:
            payload = {"text": message}
            response = requests.post(self.webhook_url, headers=HEADERS, json=payload)
            response.raise_for_status()
            logger.info("Message successfully sent to Teams.")
        except requests.RequestException as e:
            logger.error(f"Error sending message to Teams: {e}")
            raise

    def send_quote_with_image(self, quote: str, author: str, image_url: str) -> None:
        """
        Sends a quote with an image to Teams.
        :param quote: The quote text.
        :param author: The author of the quote.
        :param image_url: The URL of the image.
        """
        message_data: Dict[str, Any] = {
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
                                "weight": "Bolder",
                            },
                            {
                                "type": "TextBlock",
                                "text": quote,
                                "wrap": True,
                            },
                            {
                                "type": "TextBlock",
                                "text": f"-{author}",
                                "wrap": True,
                                "size": "Medium",
                                "spacing": "Medium",
                            },
                            {
                                "type": "Image",
                                "url": image_url,
                                "size": "Stretch",
                            },
                        ],
                    },
                },
            ],
        }

        try:
            response = requests.post(self.webhook_url, headers=HEADERS, json=message_data)
            response.raise_for_status()
            logger.info(f"Message sent successfully. Code: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Error sending message to Teams: {e}")
            raise
