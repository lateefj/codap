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
