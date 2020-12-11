# TODO check these lists resources
# List of exclusive SYSDAMIN role policies
# The role SYSADMIN is exclusive for DEFAULT application
SYSADMIN_EXCLUSIVE_POLICIES = [
    ('/applications', ['POST']),
    ('/applications/<id>', ['PUT', 'DELETE']),

    ('/domains', ['POST', 'GET']),
    ('/domains/<id>', ['DELETE']),

    ('/capabilities', ['POST']),
    ('/capabilities/<id>', ['PUT', 'DELETE']),

    ('/policies', ['POST']),
    ('/policies/<id>', ['PUT', 'DELETE']),

    ('/roles', ['POST']),
    ('/roles/<id>', ['PUT', 'DELETE']),
    ('/roles/<id>/policies', ['POST']),

    ('/routes', ['POST']),
    ('/routes/<id>', ['PUT', 'DELETE'])
]

SYSADMIN_RESOURCES = [
    ('/applications', ['GET']),
    ('/applications/<id>', ['GET']),
    ('/applications/<id>/roles', ['GET']),

    ('/domains/<id>', ['PUT', 'GET']),
    ('/domains/<id>/settings', ['POST', 'PUT', 'DELETE']),
    ('/domains/<id>/logo', ['PUT', 'DELETE']),

    ('/capabilities', ['GET']),
    ('/capabilities/<id>', ['GET']),

    ('/policies', ['GET']),
    ('/policies/<id>', ['GET']),

    ('/roles', ['GET']),
    ('/roles/<id>', ['GET']),

    ('/images', ['POST', 'GET']),
    ('/images/<id>', ['PUT', 'DELETE']),

    ('/files', ['POST', 'GET']),
    ('/files/<id>', ['PUT', 'GET', 'DELETE']),

    ('/routes', ['POST', 'GET']),
    ('/routes/<id>', ['PUT', 'GET', 'DELETE']),

    ('/grants', ['POST', 'GET']),
    ('/grants/<id>', ['PUT', 'GET', 'DELETE']),

    ('/notifications', ['POST', 'GET']),
    ('/notifications/<id>', ['PUT', 'GET', 'DELETE']),

    ('/tags', ['POST', 'GET']),
    ('/tags/<id>', ['PUT', 'GET', 'DELETE']),

    ('/tokens', ['GET']),
    ('/tokens/<id>', ['DELETE']),

    ('/users', ['POST', 'GET']),
    ('/users/<id>', ['DELETE']),
    ('/users/<id>/reset', ['POST'])
]

# Common resources for all users
USER_RESOURCES = [
    ('/tokens', ['POST']),
    ('/tokens/<id>', ['GET', 'DELETE']),
    ('/applications/<id>', ['GET']),
    ('/domains/<id>', ['GET']),
    ('/domains/<id>/settings', ['GET']),
    ('/images/<id>', ['GET']),

    ('/users/<id>', ['GET', 'PUT']),
    ('/users/<id>/photo', ['PUT', 'DELETE']),
    ('/users/<id>/notify', ['POST']),
    ('/users/<id>/update_my_password', ['PUT']),
    ('/users/routes', ['GET']),
    ('/users/reset', ['POST'])
]
