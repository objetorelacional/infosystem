import flask
import uuid
import os
from werkzeug import utils as werkzeug_utils

from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation


# TODO(samueldmq): put this in the app config
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_upload_folder(domain_id):
    base_folder = os.environ.get('INFOSYSTEM_FILE_DIR', UPLOAD_FOLDER)
    working_directory = os.getcwd()
    folder = os.path.join(working_directory, base_folder, domain_id)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


class Create(operation.Create):

    def __call__(self, file, domain_id, **kwargs):
        self.file = file
        self.domain_id = domain_id
        return super().__call__(**kwargs)

    def pre(self, session, **kwargs):
        if self.file and allowed_file(self.file.filename):
            filename = werkzeug_utils.secure_filename(self.file.filename)
            self.entity = self.driver.instantiate(
                id=uuid.uuid4().hex, domain_id=self.domain_id, name=filename)
        else:
            # NOTE(samueldmq): this will force a 400 since the name is not
            # provided, raise specific exception here about the file
            self.entity = self.driver.instantiate(
                id=uuid.uuid4().hex, domain_id=self.domain_id)

        return self.entity.is_stable()

    def do(self, session, **kwargs):
        folder = get_upload_folder(self.domain_id)
        self.file.save(os.path.join(folder, self.entity.filename))
        entity = super().do(session)
        return entity


class Get(operation.Get):

    def do(self, session, **kwargs):
        file = super().do(session, **kwargs)

        folder = get_upload_folder(file.domain_id)
        return flask.send_from_directory(folder, file.filename)


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create = Create(self)
        self.get = Get(self)
