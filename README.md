codap
=====

There are basically three simple data access patterns that this abstraction is for. The common component is a callback that will be run concurrently with the response stored into a datastructure.

Key / Value (Dictionary)
------------------------

Allows for a dictionary like access.

<pre><code class="python">
results = KV()
results['foo'] = bar # bar is a function
results.put('cats', get_photos, id, limit=4) # get_photos is a function
results.put('monkey', back, db, name)
render_template('my_temp.html', **results)
</code></pre>

Ordered List
------------

List that returns the responses based on the order they are added.

<pre><code class="python">
results = codap.Ordered()
for x in xrange(0, 10):
  results.push(get_stuff, db, x)
for r in results: # Same order as pushed
</code></pre>

First Reply
-----------

Based on the order of the response is the order it is added to the list.

<pre><code class="python">
fr = codap.FirstReply()
for ds in datasource_list:
  fr.push(get_data, id)
data = fr[0]
</code></pre>


