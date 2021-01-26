import uuid
import flask
import sqlalchemy

# TODO this import here is so strange
from datetime import datetime
from infosystem import database
from infosystem.common import exception


class Operation(object):

    def __init__(self, manager):
        self.manager = manager
        self.driver = manager.driver if hasattr(manager, 'driver') else None

    def pre(self, **kwargs):
        return True

    def do(self, **kwargs):
        return True

    def post(self):
        pass

    def __call__(self, **kwargs):
        session = kwargs.pop('session', database.db.session)

        if not self.pre(session=session, **kwargs):
            raise exception.PreconditionFailed()

        if not getattr(session, 'count', None):
            setattr(session, 'count', 0)

        session.count += 1

        try:
            result = self.do(session, **kwargs)
            session.count -= 1

            if session.count == -1:
                # raise exception.FatalError
                print('ERRO! SESSION COUNT COULD NOT BE -1')

            if session.count == 0:
                session.commit()
            self.post()
        except sqlalchemy.exc.IntegrityError as e:
            session.rollback()
            session.count -= 1
            msg_info = ''.join(e.args)
            raise exception.DuplicatedEntity(msg_info)
        except Exception as e:
            session.rollback()
            session.count -= 1
            raise e
        return result


class Create(Operation):

    def pre(self, session, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = uuid.uuid4().hex
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now()
        if 'created_by' not in kwargs:
            if flask.has_request_context():
                token_id = flask.request.headers.get('token')
                if token_id is not None:
                    self.token = self.manager.api.tokens.get(id=token_id)
                    kwargs['created_by'] = self.token.user_id

        self.entity = self.driver.instantiate(**kwargs)

        return self.entity.is_stable()

    def do(self, session, **kwargs):
        self.driver.create(self.entity, session=session)
        return self.entity


class Get(Operation):

    def pre(self, session, id, **kwargs):
        self.id = id
        return True

    def do(self, session, **kwargs):
        entity = self.driver.get(self.id, session=session)
        return entity


class List(Operation):

    def do(self, session, **kwargs):
        entities = self.driver.list(session=session, **kwargs)
        return entities


class Update(Operation):

    def pre(self, session, id, **kwargs):
        if id is None:
            raise exception.BadRequest

        self.entity = self.driver.get(id, session=session)

        self.entity.updated_at = datetime.now()
        if 'updated_by' not in kwargs:
            if flask.has_request_context():
                token_id = flask.request.headers.get('token')
                if token_id is not None:
                    self.token = self.manager.api.tokens.get(id=token_id)
                    self.entity.updated_by = self.token.user_id

        return self.entity.is_stable()

    def do(self, session, **kwargs):
        self.driver.update(self.entity, kwargs, session=session)
        return self.entity


class Delete(Operation):

    def pre(self, session, id, **kwargs):
        self.entity = self.driver.get(id, session=session)
        return True

    def do(self, session, **kwargs):
        self.driver.delete(self.entity, session=session)


class Count(Operation):

    def do(self, session, **kwargs):
        rows = self.driver.count(session=session)
        return rows
