import json
import testtools
import uuid

import infosystem


class InfoSystemTest(object):

    def setUp(self):
        super(InfoSystemTest, self).setUp()
        app = infosystem.SystemFlask()
        app.config['TESTING'] = True
        self.app = app.test_client()

        response = self.app.post(
            '/tokens',
            data=json.dumps({'domain_name': 'default', 'username': 'admin', 'password': '123456'}),
            headers={'Content-Type': 'application/json'})

        self.token = json.loads(response.data.decode())['token']['id']

        self.load_fixtures()

    def load_fixtures(self):
        pass

    @property
    def resource_name(self):
        return NotImplemented

    @property
    def collection_name(self):
        return self.resource_name + 's'

    @property
    def required_attributes(self):
        return NotImplemented

    @property
    def optional_attributes(self):
        return []

    @property
    def unique_attributes(self):
        return NotImplemented

    @property
    def hidden_attributes(self):
        return []

    def new_resource_ref(self):
        return NotImplemented

    def check_resource(self, resource, ref=None):
        resource_copy = resource.copy()

        resource_id = resource_copy.pop('id')
        self.assertEqual(uuid.UUID(resource_id, version=4).hex,
                         resource_id)

        if ref:
            # Drop hidden attributes before comparing
            for attr in self.hidden_attributes:
                ref.pop(attr)

            if 'id' in ref:
                self.assertEqual(resource_id, ref.pop('id'))

            self.assertDictEqual(resource_copy, ref)
        else:
            attrs = (attr for attr in self.required_attributes if attr not in self.hidden_attributes)
            for attr in attrs:
                self.assertIsNotNone(resource_copy[attr])

    def post(self, resource_ref, status='201 CREATED',
             resource_name=None, collection_name=None,
             headers=None):
        if resource_name is None:
            resource_name = self.resource_name
        if collection_name is None:
            collection_name = self.collection_name
        if headers is None:
            headers = {'token': self.token,
                       'Content-Type': 'application/json'}

        if resource_ref is not None:
            resource_ref = json.dumps(resource_ref)

        response = self.app.post(
            '/' + collection_name,
            headers=headers,
            data=resource_ref)

        self.assertEqual(status, response.status)

        if status == '201 CREATED':
            return json.loads(response.data.decode())[resource_name]

    def get(self, resource_id, status='200 OK', headers=None):
        resource_path = '/' + resource_id

        if headers is None:
            headers = {'token': self.token}

        response = self.app.get(
            '/' + self.collection_name + resource_path,
            headers=headers)

        self.assertEqual(status, response.status)

        if status == '200 OK':
            return json.loads(response.data.decode())[self.resource_name]

    def list(self, status='200 OK', headers=None, **kwargs):
        for k,v in kwargs.items():
            if isinstance(v, bool):
                kwargs[k] = 'true' if v else 'false'
            elif v is None:
                kwargs[k] = 'null'
        params = '&'.join([k + '=' + str(v) for k, v in kwargs.items()])
        params = '?' + params if params else ''

        if headers is None:
            headers = {'token': self.token}

        response = self.app.get(
            '/' + self.collection_name + params,
            headers=headers)

        self.assertEqual(status, response.status)

        if status == '200 OK':
            return json.loads(response.data.decode())[self.collection_name]

    def update(self, resource_id, new_resource, status='200 OK', headers=None):
        if headers is None:
            headers = {'token': self.token,
                       'Content-Type': 'application/json'}

        response = self.app.put(
            '/%s/%s' % (self.collection_name, resource_id),
            headers=headers,
            data=json.dumps(new_resource))

        self.assertEqual(status, response.status)

        if status == '200 OK':
            return json.loads(response.data.decode())[self.resource_name]

    def delete(self, resource_id, status='204 NO CONTENT', headers=None):
        if headers is None:
            headers = {'token': self.token}
        response = self.app.delete(
            '/%s/%s' % (self.collection_name, resource_id),
            headers=headers)

        self.assertEqual(status, response.status)


class CreateTest(InfoSystemTest):

    def test_create(self):
        ref = self.new_resource_ref()
        resource = self.post(ref)
        self.check_resource(resource, ref)

    def test_create_minimal_body(self):
        ref = self.new_resource_ref()
        for attr in self.optional_attributes:
            ref.pop(attr)

        resource = self.post(ref)

        # The return is valid and the provided attrs match
        self.check_resource(resource)
        # Drop hidden attributes before comparing
        for attr in self.hidden_attributes:
            ref.pop(attr)
        self.assertDictContainsSubset(ref, resource)

    def test_create_invalid_body(self):
        ref = {uuid.uuid4().hex: uuid.uuid4().hex}
        self.post(ref, '400 BAD REQUEST')

    def test_create_incomplete_body(self):
        for attr in self.required_attributes:
            ref = self.new_resource_ref()
            ref.pop(attr)
            self.post(ref, '400 BAD REQUEST')

    def test_create_without_body(self):
        self.post(None, status='400 BAD REQUEST')

    def test_create_empty_body(self):
        self.post({}, status='400 BAD REQUEST')

    def test_create_without_token(self):
        headers = {'Content-Type': 'application/json'}

        ref = self.new_resource_ref()
        resource = self.post(ref, status='401 UNAUTHORIZED',
                             headers=headers)

    def test_create_invalid_token(self):
        headers = {'token': uuid.uuid4().hex,
                   'Content-Type': 'application/json'}

        ref = self.new_resource_ref()
        resource = self.post(ref, status='401 UNAUTHORIZED',
                             headers=headers)

    def test_create_without_content_type(self):
        headers = {'token': self.token}

        ref = self.new_resource_ref()
        resource = self.post(ref, status='400 BAD REQUEST',
                             headers=headers)

    def test_create_wrong_content_type(self):
        headers = {'Content-Type': 'application/xml',
                   'token': self.token}

        ref = self.new_resource_ref()
        resource = self.post(ref, status='400 BAD REQUEST',
                             headers=headers)


class RetrieveTest(InfoSystemTest):

    def test_get(self):
        ref = self.new_resource_ref()
        resource = self.post(ref)

        response = self.get(resource_id=resource['id'])
        self.check_resource(response, ref)

    def test_list(self):
        resources = []
        for ref in range(3):
            resources.append(self.post(self.new_resource_ref()))

        response = self.list()

        for resource in response:
            self.check_resource(resource)
        for resource in resources:
            self.assertIn(resource, response)

    def test_list_filtering_by_unique_attrs(self):
        resource = self.post(self.new_resource_ref())

        for attribute_set in self.unique_attributes:
            response = self.list(
                **{attr: resource[attr] for attr in attribute_set})
            self.assertItemsEqual([resource], response)

    def test_list_filtering_by_full_resource(self):
        resource = self.post(self.new_resource_ref())

        response = self.list(**resource)

        self.assertItemsEqual([resource], response)

    def test_list_without_token(self):
        self.list(headers={}, status='401 UNAUTHORIZED')

    def test_list_invalid_token(self):
        self.list(headers={'token': uuid.uuid4().hex},
                  status='401 UNAUTHORIZED')

    def test_get_without_token(self):
        ref = self.new_resource_ref()
        resource = self.post(ref)

        response = self.get(resource_id=resource['id'],
                            headers={},
                            status='401 UNAUTHORIZED')

    def test_get_invalid_token(self):
        ref = self.new_resource_ref()
        resource = self.post(ref)

        response = self.get(resource_id=resource['id'],
                            headers={'token': uuid.uuid4().hex},
                            status='401 UNAUTHORIZED')


class UpdateTest(InfoSystemTest):

    def test_update(self):
        ref = self.new_resource_ref()
        resource = self.post(ref)

        updated_body = resource.copy()
        updated_body['name'] = uuid.uuid4().hex

        updated_resource = self.update(resource['id'], updated_body)

        ref.update(updated_body)
        self.check_resource(updated_resource, ref)

    def test_create_without_content_type(self):
        headers = {'token': self.token}

        resource_id = uuid.uuid4().hex
        diff_body = {}
        self.update(resource_id, diff_body, status='400 BAD REQUEST',
                             headers=headers)

    def test_create_wrong_content_type(self):
        headers = {'Content-Type': 'application/xml',
                   'token': self.token}

        resource_id = uuid.uuid4().hex
        diff_body = {}
        self.update(resource_id, diff_body, status='400 BAD REQUEST',
                             headers=headers)

    def test_update_without_token(self):
        resource_id = uuid.uuid4().hex
        diff_body = {}
        self.update(resource_id, diff_body,
                    headers={}, status='401 UNAUTHORIZED')

    def test_update_invalid_token(self):
        resource_id = uuid.uuid4().hex
        diff_body = {}
        self.update(resource_id, diff_body,
                    headers={'token': uuid.uuid4().hex},
                    status='401 UNAUTHORIZED')


class DeleteTest(InfoSystemTest):

    def test_delete(self):
        ref = self.new_resource_ref()
        resource = self.post(ref)

        self.get(resource['id'])

        self.delete(resource['id'])

        self.get(resource['id'], status='404 NOT FOUND')

    def test_update_without_token(self):
        resource_id = uuid.uuid4().hex
        self.delete(resource_id,
                    headers={}, status='401 UNAUTHORIZED')

    def test_update_invalid_token(self):
        resource_id = uuid.uuid4().hex
        self.delete(resource_id,
                    headers={'token': uuid.uuid4().hex},
                    status='401 UNAUTHORIZED')


# TODO(samueldmq): Group content-type and token tests
# TODO(samueldmq): Assert what error messages actually say
# TODO(samueldmq): Use fixtures to simplify load_fixtures in classes
# TODO(samueldmq): Use local policy file for tests (with a fixture?)
# TODO(samueldmq): Test different permissions (tests for authorization)
# TODO(samueldmq): Test for token API

class CRUDTest(CreateTest, RetrieveTest, UpdateTest, DeleteTest):
    pass

