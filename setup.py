from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="app",
    version="0.0.1",
    url="https://github.com/srslynow/datastem-rest-api-template",
    author="Koen Vijverberg",
    author_email="koen@vijverb.nl",
    description="A REST API template with Flask, SQLAlchemy, Alembic, Celery and Socket.IO via a factory (create_app) function",
    packages=find_packages(exclude=("tests",)),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7"
    ],
)
