from infosystem.celery import celery
from infosystem.subsystem.domain import manager
from infosystem.subsystem.user.email import TypeEmail


@celery.task
def send_email(user_id: str) -> None:
    manager.api.users.notify(
        id=user_id, type_email=TypeEmail.ACTIVATE_ACCOUNT)
