import logging

logger = logging.getLogger(__name__)


def load_quote(**kwargs):
    quote = "It's Wednesday, my dudes"
    author = "The Manager"
    logger.info("Successfully loaded fixed quote.")
    kwargs['ti'].xcom_push(key='quote', value=quote)
    kwargs['ti'].xcom_push(key='author', value=author)
