from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlaclehmy.ext.declarative import declarative_base

from fretaggregator import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()