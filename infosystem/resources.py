# TODO check these lists resources
# List of exclusive SYSDAMIN role policies
# The role SYSADMIN is exclusive for DEFAULT application
SYSADMIN_EXCLUSIVE_POLICIES = [
    ("/applications", ["POST", "PUT", "DELETE"]),
    # ("/applications/<id>", ["GET"]),
    ("/domains", ["POST", "GET", "DELETE"]),
    ("/domains/<id>", ["PUT"]),

    ("/capabilities", ["PUT", "GET", "DELETE"]),
    ("/capabilities/<id>", ["POST", "GET"]),

    ("/policies", ["PUT", "GET", "DELETE"]),
    ("/policies/<id>", ["POST", "GET"]),

    ("/roles", ["PUT", "GET", "DELETE"]),
    ("/roles/<id>", ["POST", "GET"])

    # ("POST", "/applications"),
    # ("GET", "/applications"),
    # ("PUT", "/applications/<id>"),
    # ("DELETE", "/applications/<id>"),

    # ("POST", "/domains"),
    # ("GET", "/domains"),
    # ("DELETE", "/domains/<id>"),

    # ("POST", "/capabilities"),
    # ("PUT", "/capabilities/<id>"),
    # ("DELETE", "/capabilities/<id>"),

    # ("POST", "/policies"),
    # ("PUT", "/policies/<id>"),
    # ("DELETE", "/policies/<id>"),

    #  ("POST", "/roles"),
    #  ("PUT", "/roles/<id>"),
    #  ("DELETE", "/roles/<id>")
]

SYSADMIN_RESOURCES = [
    ("/applications", ["POST", "PUT", "GET", "DELETE"]),
    ("/domains", ["POST", "PUT", "GET", "DELETE"]),
    ("/capabilities", ["POST", "PUT", "GET", "DELETE"]),
    ("/policies", ["POST", "PUT", "GET", "DELETE"]),
    ("/roles", ["POST", "PUT", "GET", "DELETE"]),
    ("/images", ["POST", "PUT", "GET", "DELETE"]),
    ("/files", ["POST", "PUT", "GET", "DELETE"]),
    ("/routes", ["POST", "PUT", "GET", "DELETE"]),

    ("/grants", ["POST", "PUT", "GET", "DELETE"]),
    ("/notifications", ["POST", "PUT", "GET", "DELETE"]),
    ("/tags", ["POST", "PUT", "GET", "DELETE"]),
    ("/tokens", ["POST", "PUT", "GET", "DELETE"]),
    ("/users", ["POST", "PUT", "GET", "DELETE"])
]

# Common resources for all users
USER_RESOURCES = [
    ("/tokens", ["GET", "POST"]),
    ("/tokens/<id>", ["GET"]),
    ("/applications/<id>", ["GET"]),
    ("/domains/<id>", ["GET"]),
    ("/images/<id>", ["GET"]),
    ("/users/<id>", ["GET", "PUT"]),
    ("/users/<id>/photo", ["PUT", "DELETE"]),
    ("/users/<id>/notify", ["POST"]),
    ("/users/<id>/update_my_password", ["PUT"]),
    ("/users/routes", ["GET"])
]
