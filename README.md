[![Build Status](https://travis-ci.org/samueldmq/infosystem.svg?branch=master)](https://travis-ci.org/samueldmq/infosystem-ansible) [![Code Climate](https://codeclimate.com/github/samueldmq/infosystem/badges/gpa.svg)](https://codeclimate.com/github/samueldmq/infosystem) [![Test Coverage](https://codeclimate.com/github/samueldmq/infosystem/badges/coverage.svg)](https://codeclimate.com/github/samueldmq/infosystem/coverage) [![Issue Count](https://codeclimate.com/github/samueldmq/infosystem/badges/issue_count.svg)](https://codeclimate.com/github/samueldmq/infosystem)

Português Brasileiro | [English](https://github.com/objetorelacional/infosystem/blob/documentacao/README_en.md)

# InfoSystem

O Infosystem é um framework open source para criação de API REST. Ele foi
criado para dar poder ao desenvolvedor, permitindo focar no desenvolvimento do
produto e das regras de negócio em vez de problemas de engenharia.

## Começe do básico

Vamos criar um projeto básico. Primeiro, crie um arquivo chamado 'app.py' com
o seguinte conteúdo:

```python
import infosystem

system = infosystem.System()
system.run()
```

Abra um terminal e rode os seguintes comandos:

```bash
$ pip install infosystem
$ python3 app.py
```

Sua API está rodando e pronta para ser consumida. Vamos testar com uma requisição:

```bash
$ curl -i http://127.0.0.1:5000/
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 5
Server: Werkzeug/1.0.1 Python/3.7.3
Date: Thu, 15 Oct 2020 13:08:19 GMT

1.0.0%
```

Com a sua API criada, siga para nossa [documentação](https://infosystem.readthedocs.io/en/latest/) e aproveite o poder e a facilidade
do infosystem no seu negócio ou na sua nova ideia.
