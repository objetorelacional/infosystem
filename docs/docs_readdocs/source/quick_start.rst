Quickstart
==========

Ready to start the development? This page will introduce you to infosystem.


Prerequisites
-------------

- You need to have installed infosystem. If you do not, please go to :doc:`Installation <installation>`
  section.


A Todo application
------------------

In this tutorial, you will learn how to persist data in database,
how to easily create endpoints and use the security system of infosystem
provide by default.

The first step is instantiate the infosystem class. Write an 'app.py' file with
the following content:

.. code-block:: python3

  import infosystem

  system = infosystem.System()
  system.run()

Now you are ready to launch your API:

.. code-block:: console

  $ python3 app.py


And you can test your new API:

.. code-block:: console

  $ curl -i http://127.0.0.1:5000/
  HTTP/1.0 200 OK
  Content-Type: text/html; charset=utf-8
  Content-Length: 5
  Server: Werkzeug/1.0.1 Python/3.7.3
  Date: Thu, 15 Oct 2020 13:08:19 GMT

  1.0.0%

Using a database
----------------

By default the infosystem uses in memory database for development porpuses and
`sqlalchemy <https://www.sqlalchemy.org/>`_ to create the database models.
Let's create a Todo model in app.py:

.. code-block:: python3

  from infosystem.database import db # Sqlalchemy
  from infosystem.common import subsystem # Infosystem base code


  class Todo(subsystem.entity.Entity, db.Model):
      attributes = ['description', 'done']
      attributes += subsystem.entity.Entity.attributes

      # Model data provided by sqlalchemy
      description = db.Column(db.String(100), nullable=False)
      done = db.Column(db.Boolean, default=False, nullable=False)

      def __init__(self, id, description, done=False,
                  active=True, created_at=None, created_by=None,
                  updated_at=None, updated_by=None, tag=None):
          super().__init__(id, active, created_at, created_by,
                          updated_at, updated_by, tag)
          self.description = description
          self.done = done

You can think: Where the attributes active, created_at, created_by, updated_at,
updated_by and tag came from? These attributes repeatedly appears in web 
development routine. So, the Infosystem by default insert this informations
into models.


Creating a route
----------------

The infosystem already has some routes ready to give power to the programmer
during the development of the application. They are:

- /tokens

All routes created by infosystem have already implemented the methods
GET, POST, PUT, DELETE.

To create the REST urls and proccess them, let's add on our app.py:

.. code-block:: python3

  todo_subsystem = subsystem.Subsystem(resource=Todo)

  system = infosystem.System(todo_subsystem)


REST urls obey a pattern and the infosystem create all this urls and his
controllers. You just need to pass the entity to subsystem object and it's done.

Now, your app.py looks like:

.. code-block:: python3

  import infosystem

  from infosystem.database import db
  from infosystem.common import subsystem


  class Todo(subsystem.entity.Entity, db.Model):
      attributes = ['description', 'done']
      attributes += subsystem.entity.Entity.attributes

      # Model data provided by sqlalchemy
      description = db.Column(db.String(100), nullable=False)
      done = db.Column(db.Boolean, default=False, nullable=False)

      def __init__(self, id, description, done=False,
                  active=True, created_at=None, created_by=None,
                  updated_at=None, updated_by=None, tag=None):
          super().__init__(id, active, created_at, created_by,
                          updated_at, updated_by, tag)
          self.description = description
          self.done = done


  todo_subsystem = subsystem.Subsystem(resource=Todo)


  system = infosystem.System(todo_subsystem)
  system.run()


Your new url point is now acessible by "http://127.0.0.1:5000/todos".

The route names are created by the following logic: model_name + 's'


Security
--------

Today, more than never we need to take care of the security of web app. Infosystem
by default protect every route and requires a token in the requisition. For
receive the token, you need a user to authenticate. The system create automatically
a user named sysadmin and through it you will get the token.

.. note::

  In a production enviroment, it is higly recommended to change the password and the name
  of the sysadmin user for security concerns.

To get the token:

.. code-block:: bash

  $ curl -s -X POST http://127.0.0.1:5000/tokens -H "Content-Type: application/json" --data '{
        "username": "sysadmin",
        "password": "123456",
        "domain_name": "default"
    }' | python -mjson.tool

The result of the requisition:

.. code-block:: json

  {
    "token": {
        "active": true,
        "created_at": "2020-10-23T10:30:10.132787Z",
        "created_by": "442082c1b6684ce3a5aa972dde6667a9",
        "id": "8b439b7c315a47c0962053a671f0456a",
        "user_id": "442082c1b6684ce3a5aa972dde6667a9"
    }
  }

Set the id token in requisition header and your API is ready to be consumed.

Manipulating todo data
----------------------

Let's check with a GET on our TODO url:

.. code-block:: bash

  $ curl -s http://127.0.0.1:5000/todos -H 'Content-Type: application/json' -H 'token: 8b439b7c315a47c0962053a671f0456a' | python -mjson.too

And we will receive a response:

.. code-block:: json

  {
    "todos": []
  }

It's working.

.. note::

  In case these steps did not work, add a '-i' parameter in curl to see what is wrong.
  If it is a 401 error, the problem is in the token. Ajust the format, remove the quotation marks
  if you accidentally added in curl header or get a new token if you restart the server.

To create a todo, make a post to http://127.0.0.1:5000/todos with the properties
of the model you want to insert:

.. code-block:: bash

  $ curl -s http://127.0.0.1:5000/todos -H 'Content-Type: application/json' -H 'token: 8b439b7c315a47c0962053a671f0456a' --data '{
    "description": "New feature"
  }' | python -mjson.tool

And the result will be: 

.. code-block:: json

  {
      "todo": {
          "active": true,
          "created_at": "2020-10-23T11:37:24.349205Z",
          "created_by": "442082c1b6684ce3a5aa972dde6667a9",
          "description": "New feature",
          "done": false,
          "id": "49c3c5efaca14f4ea30a8a79320c220b"
      }
  }

If we make a GET to /todos:

.. code-block:: bash

  $ curl -s http://127.0.0.1:5000/todos -H 'Content-Type: application/json' -H 'token: 8b439b7c315a47c0962053a671f0456a' | python -mjson.tool


The new todo task is there:

.. code-block:: json

  {
    "todos": [
      {
        "description": "New feature",
        "done": false,
        "id": "49c3c5efaca14f4ea30a8a79320c220b",
        "active": true,
        "created_at": "2020-10-23T11:37:24.349205Z",
        "created_by": "442082c1b6684ce3a5aa972dde6667a9"
      }
    ]
  }

During the day, you will finish the task and need change the state it state. To change
the resource state, we have the http method PUT. Let's make a PUT:

.. code-block:: bash

  $ curl -s -X PUT http://127.0.0.1:5000/todos/49c3c5efaca14f4ea30a8a79320c220b -H 'Content-Type: application/json' -H 'token: 8b439b7c315a47c0962053a671f0456a' --data '{
    "id": "49c3c5efaca14f4ea30a8a79320c220b",
    "done": true
  }' | python -mjson.tool

And the result:

.. code-block:: json

  {
    "todo": {
      "description": "New feature",
      "done": true,
      "id": "49c3c5efaca14f4ea30a8a79320c220b",
      "active": true,
      "created_at": "2020-10-23T11:37:24.349205Z",
      "created_by": "442082c1b6684ce3a5aa972dde6667a9",
      "updated_at": "2020-10-23T12:09:02.227455Z",
      "updated_by": "442082c1b6684ce3a5aa972dde6667a9"
    }
  }

Looking at the GET request:

.. code-block:: bash

  $ curl -s http://127.0.0.1:5000/todos -H 'Content-Type: application/json' -H 'token: 8b439b7c315a47c0962053a671f0456a' | python -mjson.tool

You will see the change in "done" propertie:

.. code-block:: json

  {
    "todos": [
      {
          "description": "New feature",
          "done": true,
          "id": "49c3c5efaca14f4ea30a8a79320c220b",
          "active": true,
          "created_at": "2020-10-23T11:37:24.349205Z",
          "created_by": "442082c1b6684ce3a5aa972dde6667a9",
          "updated_at": "2020-10-23T12:09:02.227455Z",
          "updated_by": "442082c1b6684ce3a5aa972dde6667a9"
      }
    ]
  }

With the time passing, maybe you want to delete the task. No problem. Send a DELETE:

.. code-block:: bash

  $ curl -s -X DELETE http://127.0.0.1:5000/todos/49c3c5efaca14f4ea30a8a79320c220b -H 'Content-Type: application/json' -H 'token: 8b439b7c315a47c0962053a671f0456a'

Looking again at the GET request:

.. code-block:: bash

  $ curl -s http://127.0.0.1:5000/todos -H 'Content-Type: application/json' -H 'token: 8b439b7c315a47c0962053a671f0456a' | python -mjson.tool

We have:

.. code-block:: json

  {
    "todos": []
  }

Congratulations. You have done your own CRUD with Todo list. To learn more about
infosystem informations, you can visit our reference.