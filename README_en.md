[![Build Status](https://travis-ci.org/samueldmq/infosystem.svg?branch=master)](https://travis-ci.org/samueldmq/infosystem-ansible) [![Code Climate](https://codeclimate.com/github/samueldmq/infosystem/badges/gpa.svg)](https://codeclimate.com/github/samueldmq/infosystem) [![Test Coverage](https://codeclimate.com/github/samueldmq/infosystem/badges/coverage.svg)](https://codeclimate.com/github/samueldmq/infosystem/coverage) [![Issue Count](https://codeclimate.com/github/samueldmq/infosystem/badges/issue_count.svg)](https://codeclimate.com/github/samueldmq/infosystem)

# InfoSystem

InfoSystem is a opensource framework for REST API development. It was created
for give power to the developer,allowing you to focus on product development
and business rules instead of engineering problems.

## Let's Start

Let's build a basic project. First, create a file called 'app.py' with the
following content:

```python
import infosystem

system = infosystem.System()
system.run()
```

Open a terminal and run the following commands:

```bash
$ pip install infosystem
$ python3 app.py
```

Your API is ready to be consumed. Let's test with a requisition:

```bash
$ curl -i http://127.0.0.1:5000/
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 5
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Thu, 15 Oct 2020 13:08:19 GMT

1.0.0%
```

With your API created, follow to our
[documentation](https://infosystem.readthedocs.io/en/latest/) and enjoy the
power and ease of the infosystem  for your business or your new idea.
