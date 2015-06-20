import datetime

from sqlalchemy import Column, Integer, String, DateTime

from .database import Base, engine

class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True)
  email = Column(string(256), unique=True, nullable=False)
  firstname = Column(string(128), nullable=False)
  lastname = Column(string(128), nullable=False)
  password = Column(string(128))
  
class Submission(Base):
  __tablename__ = "submissions"
  pass