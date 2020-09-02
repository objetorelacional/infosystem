from setuptools import setup, find_packages

REQUIRED_PACKAGES = [
    'apscheduler',
    'flask',
    'flask-sqlalchemy',
    'flask-rbac',
    'gabbi',
    'pika',
    'sparkpost',
    'celery==4.4.3',
    'pillow'
]

setup(
    name='infosystem',
    version='0.2.12',
    summary='Infosystem Framework',
    url='https://github.com/objetorelacional/infosystem',
    author='Samuel de Medeiros Queiroz, Francois Oliveira',
    author_email='samueldmq@gmail.com, oliveira.francois@gmail.com',
    license='Apache-2',
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED_PACKAGES
)
