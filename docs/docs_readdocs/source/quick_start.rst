Quickstart
==========

Ready to start the development? This page will introduce you to infosystem.


Prerequisites
-------------

- You need to have installed infosystem. If you do not, please go to :doc:`Installation <installation>`
  section.


A Todo application
------------------

The first step is instantiate the infosystem class. Write an 'app.py' file with
the following content:

.. code-block:: python3

  import infosystem

  system = infosystem.System()
  system.run()

Now you are ready to launch your API:

.. code-block:: console

  $ python3 app.py


And you can consume your new API:

.. code-block:: console

  $ curl -i http://127.0.0.1:5000/
  HTTP/1.0 200 OK
  Content-Type: text/html; charset=utf-8
  Content-Length: 5
  Server: Werkzeug/1.0.1 Python/3.7.3
  Date: Thu, 15 Oct 2020 13:08:19 GMT

  1.0.0%
