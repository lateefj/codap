import time
import urllib2
import json
import codap
def order_pass(order, url):
    start = time.time()
    data = urllib2.urlopen(url)
    end = time.time()
    return data, order, end - start
URL = 'https://twitter.com/status/user_timeline/lateefjackson.json?count=10 '
start = time.time()
fr = codap.FirstReply()
#fr = codap.Ordered()
count = 0
fr.push(order_pass, count, URL)
for x in xrange(0, 10):
    count += 1
    fr.push(order_pass, count, URL)
resp, c, t = fr.next()
data = json.loads(resp.read())
end = time.time()
total_statuses = len(data)
print('Getting it once time is: {0} with statuses {1}'.format(t, total_statuses))
loop_time = time.time()
c = 0
for resp, order, t in fr:
    data = json.loads(resp.read())
    end = time.time()
    print('Order: {3} getting it {2} time is: {0} with statuses {1}'.format(t, total_statuses, c, order))
    c += 1
    total_statuses += len(data)
end = time.time()
print('For 10 gets {0} with total statuses: {1} '.format(end - loop_time, total_statuses))

print('Total time is {0}'.format(end - start))
