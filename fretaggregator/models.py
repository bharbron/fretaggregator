import datetime
from flask.ext.login import UserMixin

from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base, engine, session

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
  
class Video(Base):
  __tablename__ = "videos"
  id = Column(Integer, primary_key=True)
  video_id = Column(String(256), nullable=False)
  timestamp = Column(Integer, default=0)
  
  submissions = relationship("Submission", backref="video")
  
  def as_link(self):
    return "https://youtu.be/{0}?t={1}".format(self.video_id, self.timestamp)
  
  def as_embedded(self, show_controls=False, show_title=False):
    if show_controls:
      controls = ""
    else:
      controls = "&controls=0"
    if show_title:
      title = ""
    else:
      title = "&showinfo=0"
    return "https://www.youtube.com/embed/{0}?start={1}&rel=0{2}{3}".format(self.video_id, self.timestamp, controls, title)
  
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
  video_id = Column(Integer, ForeignKey('videos.id'), nullable=False)
  guitarist_id = Column(Integer, ForeignKey('guitarists.id'))
  videoguitarist_id = Column(Integer, ForeignKey('videoguitarists.id'))
  
  ratings = relationship("Rating", backref="submission")
  
  def count_thumbs_up(self):
    return session.query(Rating).filter_by(thumbs_up = True, submission_id = self.id).count()
    
  def count_thumbs_down(self):
    return session.query(Rating).filter_by(thumbs_up = False, submission_id = self.id).count()