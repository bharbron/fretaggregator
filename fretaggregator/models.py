import datetime
from flask.ext.login import UserMixin

from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base, engine

class User(Base, UserMixin):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True)
  email = Column(String(256), unique=True, nullable=False)
  firstname = Column(String(128), nullable=False)
  lastname = Column(String(128), nullable=False)
  password = Column(String(128), nullable=False)
  
  submissions = relationship("Submission", backref="submitter")
  ratings = relationship("Rating", backref="rater")
  
class Song(Base):
  __tablename__ = "songs"
  id = Column(Integer, primary_key=True)
  title = Column(String(512), nullable=False)
  
  band_id = Column(ForeignKey('bands.id'), nullable=False)
  
  submissions = relationship("Submission", backref="song")
  
class Band(Base):
  __tablename__ = "bands"
  id = Column(Integer, primary_key=True)
  name = Column(String(256), unique=True, nullable=False)
  
  submissions = relationship("Submission", backref="band")
  songs = relationship("Song", backref="band")
  
class Guitarist(Base):
  __tablename__ = "guitarists"
  id = Column(Integer, primary_key=True)
  name = Column(String(256), unique=True, nullable=False)
  
  submissions = relationship("Submission", backref="guitarist")
  
class VideoGuitarist(Base):
  __tablename__ = "videoguitarists"
  id = Column(Integer, primary_key=True)
  name = Column(String(256), unique=True, nullable=False)
  
  submissions = relationship("Submission", backref="videoguitarist")
  
class Link(Base):
  __tablename__ = "links"
  id = Column(Integer, primary_key=True)
  url = Column(String(256))
  timestamp = Column(Integer, default=0)
  
  submissions = relationship("Submission", backref="link")
  
class Rating(Base):
  __tablename__ = "ratings"
  id = Column(Integer, primary_key=True)
  thumbs_up = Column(Boolean, nullable=False)
  
  rater_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
  
class Submission(Base):
  __tablename__ = "submissions"
  id = Column(Integer, primary_key=True)
  submission_date = Column(DateTime, default=datetime.datetime.now)
  
  submitter_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)
  band_id = Column(Integer, ForeignKey('bands.id'), nullable=False)
  link_id = Column(Integer, ForeignKey('links.id'), nullable=False)
  guitarist_id = Column(Integer, ForeignKey('guitarists.id'))
  videoguitarist_id = Column(Integer, ForeignKey('videoguitarists.id'))
  
  ratings = relationship("Rating", backref="submission")