import base64
import logging

import requests
from airflow.models import Variable

logger = logging.getLogger(__name__)


def send_to_teams(**kwargs):
    image_local_path = kwargs["ti"].xcom_pull(key="image_local_path")
    webhook_url = Variable.get("webhook_url")

    with open(image_local_path, "rb") as image_file:
        image_data = image_file.read()

    image_base64 = base64.b64encode(image_data).decode("utf-8")

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
                            "weight": "Bolder",
                        },
                        {
                            "type": "Image",
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "size": "Stretch",
                        },
                    ],
                },
            },
        ],
    }

    response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, json=message_data)
    response.raise_for_status()
    logger.info("Message successfully sent to Teams.")
