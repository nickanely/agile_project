import logging

import requests
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
