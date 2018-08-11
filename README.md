#About
Logging page time generation and SQLAlchemy requests. 

##Quick Start
Install profiler by git.
```python
git clone https://github.com/slivetssergey/flask-alchemy-profiler.git
```


###Initialization
```python
from profiler import FlaskProfiler
profiler = FlaskProfiler()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    profiler.init_app(app)
    .....
```