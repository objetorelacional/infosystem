from gabbi import fixture

import abc
import json
import uuid
import infosystem
import os


class Fixture(fixture.GabbiFixture):

    def __init__(self):
        super().__init__()

        self.system = infosystem.SystemFlask()
        self.app = self.system.test_client()

    @property
    def individual(self):
        return None

    @property
    def collection(self):
        return self.individual + 's'

    @abc.abstractmethod
    def new_dict(self):
        raise NotImplementedError

    def start_fixture(self):
        if self.individual == 'token':
            headers = {'Content-Type': 'application/json'}
        else:
            headers = {'token': self.env('token'),
                       'Content-Type': 'application/json'}

        response = self.app.post(
            '/' + self.collection,
            headers=headers,
            data=json.dumps(self.new_dict()))

        resource = json.loads(response.data.decode())[self.individual]

        k = self.individual
        if self.env(k):
            i = 2
            while self.env(k + '.' + str(i)):
                i += 1
            k = k + '.' + str(i)

        self.key = k
        self.value = resource['id']

        self.env(self.key, self.value)

    def stop_fixture(self):
        if self.collection == 'tokens':
            return
        headers = {'token': self.env('token'),
                   'Content-Type': 'application/json'}
        self.app.delete('/' + self.collection + '/' + self.value,
                        headers=headers)
        os.environ.pop(self.key)

    def env(self, k, v=None):
        if v is not None:
            os.environ[k] = v
        else:
            try:
                v = os.environ[k]
            except KeyError:
                v = None
        return v


class TokenFixture(Fixture):

    @property
    def individual(self):
        return 'token'

    def new_dict(self):
        return {'domain_name': 'default',
                'username': 'admin',
                'password': '123456'}


class DomainFixture(Fixture):

    @property
    def individual(self):
        return 'domain'

    def new_dict(self):
        return {'name': uuid.uuid4().hex}


class UserFixture(Fixture):

    @property
    def individual(self):
        return 'user'

    def new_dict(self):
        return {'domain_id': self.env('domain'),
                'name': uuid.uuid4().hex,
                'email': uuid.uuid4().hex,
                'password': uuid.uuid4().hex}
