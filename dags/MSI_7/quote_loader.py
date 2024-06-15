import logging

import requests
from airflow.exceptions import AirflowException
from airflow.providers.http.hooks.http import HttpHook

logger = logging.getLogger(__name__)


def load_quote(**kwargs):
    http = HttpHook(http_conn_id="quote_api", method="GET")
    try:
        response = http.run(endpoint="")
        data = response.json()
        quote = data.get("content")
        author = data.get("author")
        if quote is None or author is None:
            raise Exception("Incomplete data received.")
        logger.info(f"Successfully loaded quote - {quote}")
        kwargs["ti"].xcom_push(key="quote", value=quote)
        kwargs["ti"].xcom_push(key="author", value=author)
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        raise AirflowException(f"Failed to load quote: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception: {e}")
        raise AirflowException(f"Failed to load quote: {e}")
