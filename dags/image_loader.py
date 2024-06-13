import logging
import os
import textwrap
import uuid
from io import BytesIO

import requests
from PIL import Image, ImageDraw
from airflow.exceptions import AirflowException
from airflow.providers.http.hooks.http import HttpHook

logger = logging.getLogger(__name__)


def load_image(**kwargs):
    http = HttpHook(http_conn_id="image_api", method="GET")

    try:
        response = http.run(endpoint="")
        response.raise_for_status()
        image_url = response.url
        logger.info("Successfully loaded image URL.")
        kwargs["ti"].xcom_push(key="image_url", value=image_url)
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        raise AirflowException(f"Failed to load image: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception: {e}")
        raise AirflowException(f"Failed to load image: {e}")

    response = requests.get(image_url)
    if response.status_code != 200:
        raise AirflowException(f"Failed to download image: {response.status_code}")

    image = Image.open(BytesIO(response.content))

    quote = kwargs["ti"].xcom_pull(task_ids="load_quote", key="quote")
    author = kwargs["ti"].xcom_pull(task_ids="load_quote", key="author")

    draw = ImageDraw.Draw(image)

    text = f"{quote}\n- {author}"
    text_color = "black"

    wrapped_text = textwrap.fill(text, width=40)
    text_position = (10, 10)
    draw.multiline_text(text_position, wrapped_text, fill=text_color)

    image_filename = f"random_image_{uuid.uuid4().hex}.jpg"
    image_dir = "agile_project/data"
    image_path = os.path.join(image_dir, image_filename)

    os.makedirs(image_dir, exist_ok=True)

    image.save(image_path)

    kwargs["ti"].xcom_push(key="image_local_path", value=image_path)
    logger.info("Successfully loaded and saved image with quote locally.")
