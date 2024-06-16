import logging

from airflow.models import Variable

logger = logging.getLogger(__name__)


def load_image(**kwargs):
    toad_image_url = Variable.get('toad_image_url')
    logger.info("Successfully loaded toad image URL from Airflow Variable.")
    kwargs['ti'].xcom_push(key='image_url', value=toad_image_url)
