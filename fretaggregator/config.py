import os

class DevelopmentConfig(object):
  SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/fretaggregator"
  DEBUG = True
  SECRET_KEY = os.environ.get("FRETAGGREGATOR_SECRET_KEY", "")
  
class HerokuConfig(object):
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")
  DEBUG = False
  SECRET_KEY = os.environ.get("FRETAGGREGATOR_SECRET_KEY", "")