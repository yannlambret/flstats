flstats
=======

A performance monitoring tool for the Flask microframework.

Work in progress, hasn't been tested under heavy load yet. Suggestions and contributions are more than welcome.

A simple example of how to use it based on the [Flask][flask] documentation:

```python
from flask import Flask
from flstats import statistics, webstatistics

app = Flask(__name__)
app.register_blueprint(webstatistics)

@app.route("/")
@statistics
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
```

And that's it, your application now collects statistics that you can access at 'http://localhost:5000/flstats/'.

Data are in the JSON format, so you will get something like this:

    [{"url": "http://localhost:5000/", "count": 75, "max": 282.26, "avg": 72.0, "min": 61.07}]
    
Well, to be honest, if you run the previous code sample on a reasonably modern hardware, you will more likely get
something like this:

    [{"url": "http://localhost:5000/", "count": 75, "max": 0.0, "avg": 0.0, "min": 0.0}]
    
But you get the idea! Each stat "object" have five fields:

 - url : performance data are related to this specific URL
 - count : number of requests processed
 - max : longest execution time for a request
 - min : shortest execution time for a request
 - avg : average response time
    
[flask]: http://flask.pocoo.org/
