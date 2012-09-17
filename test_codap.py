import unittest

import codap


class TestKV(unittest.TestCase):

    def test_kv_get_set(self):
        kv = codap.KV()
        def two():
            return 2
        def t(n):
            return n*n
        r = xrange(0, 100)
        for x in r:
            kv[x] = two
        for x in r:
            assert kv[x] == 2, 'Expectex kv[x] to be {0} but it was {1}'.format(2, kv[x])

        # Make sure that passing params to callback works
        kv = codap.KV()
        for x in r:
            kv.put(x, t, x)
        for x in r:
            assert kv[x] == x * x, 'Expectex kv[x] to be {0} but it was {1}'.format(x * x, kv[x])
        # Test to make sure returning correct queue
        kv = codap.KV()
        queues = []
        for x in r:
            queues.append(kv.put(x, t, x))
        x = 0
        for q in queues:
            # Deterministic should make sure this works
            v = q.get()
            assert v == x * x, 'Expected q.get() to be {0} but it was {1}'.format(x * x, v)
            x += 1

        # Make sure put with just key as argument works
        kv = codap.KV()
        queues = []
        for x in r:
            q = kv.put(x)
            queues.append(q)
            q.put(two())
        for q in queues:
            v = q.get()
            assert v == 2, 'Expected q.get() to be 2 but it was {0}'.format(v)


from urllib2 import urlopen


def delay(amount):
    for x in xrange(0, amount):
        urlopen('http://google.com')  # Ok way to delay things a bit
    return amount


class TestOrdered(unittest.TestCase):

    def test_basic(self):
        size = 5
        coorder = codap.Ordered()

        def o(x):
            return x

        for x in reversed(xrange(0, size)):
            coorder.push(delay, x)

        assert len(coorder) == size, 'Expected to be the riht size'
        c = size - 1
        for v in coorder:
            assert v == c, 'Expected v to be {0} but was {1}'.format(c, v)
            c -= 1


class TestFirstReply(unittest.TestCase):

    def test_first_reply(self):
        fr = codap.FirstReply()

        def two():
            return 2
        for x in xrange(0, 100):
            fr.push(two)
        for p in fr:
            assert p == 2, 'Expected 2 but got {0}'.format(p)

        start = 0
        for x in reversed(xrange(start, 4)):
            fr.push(delay, x)

        c = start
        for x in fr:
            assert x == c, 'Expected {0} but got {1}'.format(c, x)
            c += 1
