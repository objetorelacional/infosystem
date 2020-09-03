from infosystem.celery import celery
from flask.globals import current_app
from infosystem.subsystem.user.email import TypeEmail


@celery.task
def send_email(user_id: str) -> None:
    current_app.subsystems['users'].manager.notify(
        id=user_id, type_email=TypeEmail.ACTIVATE_ACCOUNT)
