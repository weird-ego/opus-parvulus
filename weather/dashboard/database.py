from os import environ

from sqlalchemy import create_engine, MetaData


dbpath = environ['dbpath']
engine = create_engine(dbpath)
meta = MetaData(bind=engine)
meta.reflect()

subscription = meta.tables['facade_subscription']
weather_state = meta.tables['facade_weatherstate']
weather = meta.tables['facade_weather']
city = meta.tables['facade_city']
user = meta.tables['auth_user']

engine.dispose()
