from flask import Flask
from flask.globals import current_app
from celery import Celery

celery = Celery('infosystem')


def init_celery(app: Flask) -> Celery:
    celery.conf.update(broker_url=app.config['CELERY_BROKER_URL'])
    #    result_backend=app.config['CELERY_BACKEND_URL'])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def decide_on_run(fn):
    def wrapper(*args):
        should_use_worker = current_app.config['USE_WORKER']
        if should_use_worker:
            return fn.delay(*args)
        else:
            return fn(*args)
    return wrapper
