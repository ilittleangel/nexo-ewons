from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='nexo-ewons',
    version='0.1.0',
    description='Simple project to ingest tags from ewons',
    long_description=readme,
    author='Angel Rojo',
    author_email='angel.rojo.perez@gmail.com',
    url='https://github/ilittleangel/nexo-ewons.git',
    packages=find_packages(exclude=('tests', 'docs'))
)
