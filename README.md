codap
=====

[![Travis Build Status](https://api.travis-ci.org/lateefj/codap.png?branch=master)](https://travis-ci.org/lateefj/codap)

Coroutine Data Access Patterns (codap) are a handful of libraries to make concurrent data access simpler to use. This was originally developed for web services access data in mutliple datastores (MongoDB, S3, REST, ect). The library uses async methods (thread, eventlet or gevent) which degrades gracefully. Perfering gevent, eventlet and falling back to threading. One of those things it would be really nice to have anonymous functions in Python :(.

INSTALL
-------

```
pip install codap
```


Key / Value (Dictionary)
------------------------

Allows for a dictionary like access. This is great for caches, template rendering and since dictionaries are the most used data type it is easy to integrate into existing code. 

Example:

```python
def back(db, name):
  return db.find(name)

results = KV()
results['foo'] = bar # bar is a function
results.put('cats', get_photos, id, limit=4) # get_photos is a function
results.put('monkey', back, db, name)
render_template('my_temp.html', **results)
```

Ordered List
------------

List that returns the responses based on the order they are added. Has been used for retrieving already sorted data that needs additional information to be rendered.

Example:

```python

def get_stuff(db, x):
  return db.get(x)

results = codap.Ordered()
for x in xrange(0, 10):
  results.push(get_stuff, db, x)
for r in results: # Same order as pushed
  r.render()
```

First Reply
-----------

Based on the order of the response is the order it is added to the list. Useful for making request to multiple databases. Has been used for getting a list of files from a web service and compressing them into a single zip or tar.

Example:

```python

def get_data(id):
  return my_data[id]

fr = codap.FirstReply()
for ds in datasource_list:
  fr.push(get_data, id)
data = fr[0]
```

Fibonacci Example (full):
-------------------------

```python
import codap


def fib(n):
    if n == 1:
        return 1
    elif n == 0:
        return 0
    else:
        return fib(n - 1) + fib(n - 2)

FIB_SIZE = 30
d = codap.KV()
# Push a bunch of fib processing into the background
for i in range(0, FIB_SIZE):
    d.put(i, fib, i)

# Pull them out from the list
for i in range(0, FIB_SIZE):
    assert d[i] == fib(i), 'Expected fib {0} to be {1} but was {3}'.format(i, d[i], fib(i))

d = codap.Ordered()
for i in range(0, FIB_SIZE):
    d.push(fib, i)

i = 0
for f in d:
    assert f == fib(i), 'Expected fib {0} to be {1} but was {3}'.format(i, f, fib(i))
    i += 1
```

