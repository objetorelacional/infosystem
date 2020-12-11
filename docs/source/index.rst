.. InfoSystem documentation master file, created by
   sphinx-quickstart on Tue Oct 20 09:42:16 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

InfoSystem
======================================

Version 1.0.0

-----

InfoSystem is a :doc:`open source <license>` framework for REST API development. It was created
for give power to the developer,allowing you to focus on product development
and business rules instead of engineering problems.

Let's Start
-----------

Let's build a basic project. First, create a file called 'app.py' with the
following content:

.. code-block:: python3

  import infosystem

  system = infosystem.System()
  system.run()

Open a terminal and run the following commands:

.. code-block:: console

  $ pip install infosystem
  $ python3 app.py

Your API is ready to be consumed. Let's test with a requisition:

.. code-block:: console

  $ curl -i http://127.0.0.1:5000/
  HTTP/1.0 200 OK
  Content-Type: text/html; charset=utf-8
  Content-Length: 5
  Server: Werkzeug/1.0.1 Python/3.7.3
  Date: Thu, 15 Oct 2020 13:08:19 GMT

  1.0.0%


The infosystem is very concerned with the application security. It requires in
every requisition a token provided by itself. To get the token:

.. code-block:: console

    $ curl -s -X POST http://127.0.0.1:5000/tokens -H "Content-Type: application/json" --data '{
        "username": "sysadmin",
        "password": "123456",
        "domain_name": "default"
    }' | python -mjson.tool


You will receive a response like this:

.. code-block:: json

  {
    "token": {
        "user_id": "afeee5968727407f916ac094f6cdeb68",
        "id": "9fa6486d35b546de8204504dfc4f14f4",
        "active": true,
        "created_at": "2020-10-22T11:47:59.200842Z",
        "created_by": "afeee5968727407f916ac094f6cdeb68"
    }
  }


For learning more about infosystem, please follow to our :doc:`quickstart <quick_start>`
or for our references.

Feel free to contribute
-----------------------

As a open source project, anywhone who want to contribute to the project can
:doc:`send a pull request, open an issue or send an email <contribute>`.

.. note::
   Like the infosystem project, these documents are also constantly envolving.
   For any information please look at the links on the sidebar.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   license
   quick_start
   contribute
   installation
