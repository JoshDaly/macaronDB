from distutils.core import setup

setup(
    name='macaronDB',
    version='0.0.1',
    author='Michael Imelfort',
    author_email='mike@mikeimelfort.com',
    packages=['macarondb'],
    scripts=['bin/macarondb'],
    url='http://pypi.python.org/pypi/macaronDB/',
    license='GPLv3',
    description='macaronDB',
    long_description=open('README.md').read(),
    install_requires=[],
)

