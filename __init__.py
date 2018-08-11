from flask import Blueprint, request, g, render_template
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from .models import Base, Request, Query
from .functions import format_fname
import datetime
import time


__all__ = ('FlaskProfiler', )
__version__ = '0.0.1'


session = None


class FlaskProfiler(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        global session

        register_views(app)
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        # app.teardown_request(self.teardown_request)

        engine = create_engine('sqlite:///profile.sqlite')
        Base.metadata.create_all(engine)
        _s = sessionmaker(bind=engine)
        session = _s()

    @staticmethod
    def before_request():
        g.timestamp = time.time()

    @staticmethod
    def after_request(response):
        if request.path.startswith('/_debug_toolbar/') or request.path.startswith('/profiler/'):
            return response

        _request = Request(
            url=request.full_path[:-1] if request.full_path.endswith('?') else request.full_path,
            method=request.method,
            duration=time.time()-g.timestamp,
            route=request.url_rule.rule,
            created=datetime.datetime.now()
        )
        session.add(_request)

        for query in get_debug_queries():
            _query = Query(
                request=_request,
                sql=query.statement,
                duration=query.duration,
                parameters=str(query.parameters),
                context=format_fname(query.context)
            )
            session.add(_query)

        session.commit()
        return response

    def teardown_request(self, exc):
        pass


def register_views(app):

    profiler_blueprint = Blueprint(
        'profiler',
        __name__,
        url_prefix='/profiler',
        template_folder='templates',
        # template_folder='/profiler/templates/',
        # static_folder='static/dist/',
        # static_url_path='/static/dist'
    )

    @profiler_blueprint.route('/')
    def dashboard_view():

        object_list = session.query(
            Request.route,
            Request.method,
            func.avg(Request.duration).label('time_avg'),
            func.min(Request.duration).label('time_min'),
            func.max(Request.duration).label('time_max'),
            func.count(Request.id).label('count'),
        ).group_by(Request.route, Request.method)
        return render_template('profiler_index.html', object_list=object_list.all())

    @profiler_blueprint.route('/queries/')
    def queries_view():
        object_list = session.query(
            Query.sql,
            func.avg(Query.duration).label('time_avg'),
            func.min(Query.duration).label('time_min'),
            func.max(Query.duration).label('time_max'),
            func.count(Query.id).label('count')
        ).group_by(Query.sql).all()
        return render_template('profiler_queries.html', object_list=object_list)

    app.register_blueprint(profiler_blueprint)
