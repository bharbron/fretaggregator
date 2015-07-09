from flask import render_template, request, redirect, url_for

from models import Submission, Song, Band, Link, User
from fretaggregator import app
from .database import session
from helpers import get_or_create

@app.route("/", methods=["GET"])
def home():
  """ Main page of the site """
  # Get a list of the most recent submissions
  recent_submissions = session.query(Submission).order_by(Submission.submission_date.desc()).limit(3)
  return render_template("home.html",
                        recent_submissions=recent_submissions
                        )

@app.route("/results", methods=["GET"])
def results():
  pass
  #return render_template("results.html")
  
  
@app.route("/add", methods=["GET"])
def add_get():
  """ Page for adding new submissions """
  return render_template("add.html")

@app.route("/add", methods=["POST"])
def add_post():
  """ Receives the newly POSTed submission and adds it to the database """
  # Until we implement logon, set the submitter to the first user in the database
  user = session.query(User).get(1)
  
  #band = Band(name=request.form["band"])
  band = get_or_create(Band, name=request.form["band"])
  song = Song(title=request.form["song"], band=band)
  link = Link(url=request.form["url"])
  
  # TODO: Add the guitarist and video guitarist as well.
  
  submission = Submission(submitter=user, song=song, band=band, link=link)
  
  session.add_all([song, link, submission])
  session.commit()
  return redirect(url_for("home"))
  