# Copyright 2012 Lateef Jackson <lateef.jackson@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# Neither the name of Lateef Jackson nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
(codap) Coroutine Data Access Patterns

These are some utitlites classes I built for improving response time in a web service.
I used this to simplify making sequencial requests to data storage (serivices or database)
concurrent so that there would be less IO wait. Warning more traditional RDBMS may have inverse
performance compared to caches or datastores that are distributed.

"""
import sys
# Thread worst case but this will not scale well at all
if sys.version_info[0] == 3: # Python 3 different different standard library packagin
    from queue import Queue as ThreadQueue
else:
    from Queue import Queue as ThreadQueue
from threading import Thread


def thread_spawn(*args, **kwargs):
    """
    Wrapper that acts like the coroutine libraries. Nothing really to
    see here.
    """
    t = None
    if len(args) == 1 and not kwargs:
        t = Thread(target=args[0], args=())
    else:
        t = Thread(target=args[0], args=args[0:], kwargs=kwargs)
    t.start()

try:
    # Prever gevent as it would be fastest
    from gevent import spawn
    from gevent.queue import Queue
    import gevent
    gevent.monkey.patch_all()
except:
    try:
        # Eventlet we are also fans of so that would be great
        from eventlet import spawn
        from eventlet.queue import Queue
        import eventlet
        eventlet.monkey_patch(all=True)

    except:
        # Fall back to using threads
        Queue = ThreadQueue
        spawn = thread_spawn



class KV(dict):
    """
    This wrapper around a dict is mostly for to make getting the data
    however there is the ability to set the data. I have found in most
    cases that the function will need parameters and that is why the
    put function exists.
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        v = dict.__getitem__(self, key).get()
        dict.__getitem__(self, key).put(v)  # Make sure it is there next time we ask for it
        return v

    def __setitem__(self, k, v):
        """
        This is just a wrapper around the put function but allows the second
        argument to be the callback. The callback can not have any arguments
        or keywords so this has limited use.
        """
        self.put(k, v)

    def put(self, *args, **kwargs):
        """
        This is design to hanlde 3 situation
            1. Can pass just the key as the first argument and call put on queue
            that is returned.
            2. Pass key as fist argument and callback as second which will be called
            in a coroutine (or thread).
            3. Pass key as first argument and callback as second and the rest of the
            arguments and keywords will be passed to the callback.

        """
        key = args[0]
        callback = None
        args = args[1:]
        if len(args) > 0:
            callback = args[0]
            args = args[1:]
        q = Queue()
        dict.__setitem__(self, key, q)
        if callback:
            def handle():
                if args:
                    q.put(callback(*args))
                elif not args and kwargs:
                    q.put(callback(*args, **kwargs))
                else:
                    q.put(callback(*args, **kwargs))
            spawn(handle)
        return q


class Ordered:

    def __init__(self):
        self.size = 0
        self.kv = KV()
        self.index = 0

    def __add__(self, x):
        self.push(x)

    def __getitem__(self, i):
        print('{0} for in {1}'.format(i, self.kv.keys()))
        return self.kv[i]

    def __setitem__(self, k, v):
        self.kv[k] = v

    def __getslice__(self, i, j):
        return [self.kv[x] for x in xrange(i - 1, j)]

    def __delslize__(self, i, j):
        for x in xrange(i - 1, j):
            del self.kv[x]

    def __len__(self):
        return len(self.kv.keys())

    def __iter__(self):
        return self
    def __next__(self):
        v = None
        if self.index < len(self.kv.keys()):
            v = self.kv[self.index]
            self.index += 1
        else:
            self.index = 0
            raise StopIteration
        return v
    next = __next__ # Python 2.x backport

    def push(self, *args, **kwargs):
        self.kv.put(self.size, *args, **kwargs)
        self.size += 1

    append = __add__


class FirstReply:

    def __init__(self):
        self.size = 0
        self.index = 0
        self.q = Queue()

    def push(self, *args, **kwargs):
        self.size += 1
        callback = args[0]
        args = args[1:]
        if callback:
            def handle():
                if args and not kwargs:
                    self.q.put(callback(*args))
                elif not args and kwargs:
                    self.q.put(callback())
                else:
                    self.q.put(callback(*args, **kwargs))
            spawn(handle)
        return self.q

    def __len__(self):
        return self.size

    def __iter__(self):
        return self

    def __next__(self):
        v = None
        if self.index < self.size:
            v = self.q.get()
            self.index += 1
        else:
            raise StopIteration
        return v
    next = __next__ # Python 2.x backport
    __add__ = push
    append = push
