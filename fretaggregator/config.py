import os

class DevelopmentConfig(object):
  SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/fretaggregator"
  DEBUG = True
  SECRET_KEY = os.environ.get("FRETAGGREGATOR_SECRET_KEY", "")