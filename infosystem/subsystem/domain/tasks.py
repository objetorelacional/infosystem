from flask.globals import current_app

from infosystem.celery import celery, decide_on_run
from infosystem.common import exception
from infosystem.subsystem.user.email import TypeEmail


@decide_on_run
@celery.task(autoretry_for=(exception.NotFound,),
             default_retry_delay=5,
             retry_kwargs={'max_retries': 3})
def send_email(user_id: str) -> None:
    return current_app.subsystems['users'].manager.notify(
        id=user_id, type_email=TypeEmail.ACTIVATE_ACCOUNT)
