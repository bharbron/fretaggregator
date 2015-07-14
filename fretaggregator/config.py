import os

class DevelopmentConfig(object):
  SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/fretaggregator"
  DEBUG = True
  SECRET_KEY = os.environ.get("FRETAGGREGATOR_SECRET_KEY", "")
  
class HerokuConfig(object):
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgres://zcvdykrqcjbdca:7xUaDYbMf0LKCUuJ2mwPLwa32g@ec2-54-197-238-19.compute-1.amazonaws.com:5432/dbhoq2p6p7too5")
  DEBUG = False
  SECRET_KEY = os.environ.get("FRETAGGREGATOR_SECRET_KEY", "")