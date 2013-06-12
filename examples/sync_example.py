import time
import urllib2
import json

URL = 'https://twitter.com/status/user_timeline/lateefjackson.json?count=10'
start = time.time()
resp = urllib2.urlopen(URL)
data = json.loads(resp.read())
end = time.time()
total_statuses = len(data)
print('Getting it once time is: {0} with statuses {1}'.format(end - start, total_statuses))
loop_time = time.time()
c = 0
for x in xrange(0, 10):
    resp = urllib2.urlopen(URL)
    data = json.loads(resp.read())
    end = time.time()
    print('Getting it {2} time is: {0} with statuses {1}'.format(end - start, total_statuses, c))
    c += 1
    total_statuses += len(data)
end = time.time()
print('For 10 gets {0} with total statuses: {1} '.format(end - loop_time, total_statuses))

print('Total time is {0}'.format(end - start))
