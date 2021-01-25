from setuptools import setup, find_packages
from infosystem._version import version

REQUIRED_PACKAGES = [
    'apscheduler',
    'flask',
    'flask-rbac',
    'flask-sqlalchemy',
    'flask-migrate',
    'gabbi',
    'pika',
    'sparkpost',
    'celery',
    'pillow'
]

setup(
    name='infosystem',
    version=version,
    summary='Infosystem Framework',
    url='https://github.com/objetorelacional/infosystem',
    author='Samuel de Medeiros Queiroz, Francois Oliveira',
    author_email='samueldmq@gmail.com, oliveira.francois@gmail.com',
    license='Apache-2',
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED_PACKAGES
)
