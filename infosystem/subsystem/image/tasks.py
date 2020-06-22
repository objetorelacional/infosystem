from infosystem.celery import celery
from infosystem.subsystem.image.handler import ImageHandler


@celery.task
def process_image(folder: str, filename: str) -> None:
    handler = ImageHandler()
    handler.process(folder, filename)
