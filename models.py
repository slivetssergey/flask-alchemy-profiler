from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text, Float
from sqlalchemy.orm import relationship


Base = declarative_base()


class Request(Base):
    __tablename__ = "profiler_request"
    id = Column('id', Integer, primary_key=True)
    duration = Column('duration', Float)
    method = Column('method', String(10), index=True)
    route = Column('route', String(255), index=True)
    url = Column('url', Text)
    created = Column('created', DateTime)


class Query(Base):
    __tablename__ = "profiler_db_query"
    id = Column('id', Integer, primary_key=True)
    request_id = Column('request_id', Integer, ForeignKey('profiler_request.id'))
    request = relationship('Request', foreign_keys=request_id)
    sql = Column('sql', Text, index=True)
    parameters = Column('parameters', Text)
    duration = Column('duration', Float)
    context = Column('context', Text)
