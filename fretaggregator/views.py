from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from fretaggregator import app
from .models import Submission, Song, Band, Link, User
from .database import session
from .helpers import get_or_add

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
@login_required
def add_get():
  """ Page for adding new submissions """
  return render_template("add.html")

@app.route("/add", methods=["POST"])
@login_required
def add_post():
  """ Receives the newly POSTed submission and adds it to the database """
  # Until we implement logon, set the submitter to the first user in the database
  user = session.query(User).get(1)
  
  band = get_or_add(Band, name=request.form["band"])
  #song = Song(title=request.form["song"], band=band)
  #link = Link(url=request.form["url"])
  song = get_or_add(Song, title=request.form["song"], band=band)
  link = get_or_add(Link, url=request.form["url"])
  
  # TODO: Add the guitarist and video guitarist as well.
  
  submission = Submission(submitter=user, song=song, band=band, link=link)
  
  session.add(submission)
  session.commit()
  return redirect(url_for("home"))

@app.route("/login", methods=["GET"])
def login_get():
  return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
  email = request.form["email"]
  password = request.form["password"]
  user = session.query(User).filter_by(email=email).first()
  if not user or not check_password_hash(user.password, password):
    flash("Incorrect username or password", "danger")
    return redirect(url_for("login_get"))
  
@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("home"))