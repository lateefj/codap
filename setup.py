from setuptools import setup

DESCRIPTION = """Coroutine Data Access Patterns (mouthful I know) are some data
access patterns I found useful building web applications that use gevent or
evenlet. They mimic common Python data types like lists and dictionaries."""
setup(
    name = 'codap',
    version = '0.0.1',
    author = 'Lateef Jackson',
    author_email = 'lateef.jackson@gmail.com',
    description = (DESCRIPTION),
    license = 'BSD',
    keywords = 'gevent eventlet coroutine ',
    url = 'https://github.com/lateefj/codap',
    packages=['codap'],
    long_description=read('README.md'),
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Topic :: Utilities',
            'License :: BSD License',
        ],
)
