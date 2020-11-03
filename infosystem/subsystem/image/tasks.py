from infosystem.celery import celery, decide_on_run
from infosystem.subsystem.image.handler import ImageHandler


@decide_on_run
@celery.task
def process_image(folder: str, filename: str) -> None:
    handler = ImageHandler()
    handler.process(folder, filename)
