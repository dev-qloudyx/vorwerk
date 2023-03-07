# Create your tasks here
import logging
from apps.eventos.code_gen import CodeGeneration
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries':10, 'countdown': 5})
def send_message(**kwargs):
    msg = CodeGeneration.send_message(**kwargs)
    return logger.info('None') if msg is None else logger.info(msg)

