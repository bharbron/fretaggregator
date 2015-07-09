from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from fretaggregator import app
from .models import Submission, Song, Band, Link, User, Guitarist, VideoGuitarist
from .database import session
from .helpers import get_one_or_create

@app.route("/", methods=["GET"])
def home():
  """ Main page of the site """
  # Get a list of the most recent submissions
  recent_submissions = session.query(Submission).order_by(Submission.submission_date.desc()).limit(5)
  return render_template("home.html",
                        recent_submissions=recent_submissions
                        )

@app.route("/results", methods=["GET"])
def results():
  pass
  #return render_template("results.html")
  
@app.route("/search", methods=["POST"])
def search_post():
  """ Searches for submissions based on song or band name and returns a list of results """
  results = []
  return redirect(url_for("home"))
  
  
@app.route("/add", methods=["GET"])
@login_required
def add_get():
  """ Page for adding new submissions """
  return render_template("add.html")

@app.route("/add", methods=["POST"])
@login_required
def add_post():
  """ Receives the newly POSTed submission and adds it to the database """
  submitter = current_user  
  band = get_one_or_create(session, Band, name=request.form["band"])
  song = get_one_or_create(session, Song, title=request.form["song"], band=band)
  link = get_one_or_create(session, Link, url=request.form["url"])
  session.add_all([band, song, link])
  
  guitarist = None
  videoguitarist = None
  if request.form["guitarist"]:
    guitarist = get_one_or_create(session, Guitarist, name=request.form["guitarist"])
    session.add(guitarist)
  if request.form["videoguitarist"]:
    videoguitarist = get_one_or_create(session, VideoGuitarist, name=request.form["videoguitarist"])
    session.add(videoguitarist)
  
  submission = Submission(submitter=submitter,
                          song=song,
                          band=band,
                          link=link,
                          guitarist=guitarist,
                          videoguitarist=videoguitarist)
  
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
  
  login_user(user)
  return redirect(request.args.get('next') or url_for("home"))
  
@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("home"))

@app.route("/signup", methods=["GET"])
def signup_get():
  """ Sign up a new user """
  return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup_post():
  email = request.form["email"]
  firstname = request.form["firstname"]
  lastname = request.form["lastname"]
  password = request.form["password"]
  if session.query(User).filter_by(email=email).first():
    flash("User with that email address already exists", "danger")
    return redirect(url_for("signup_get"))
  
  user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password))
  session.add(user)
  session.commit()
  
  login_user(user)
  return redirect(url_for("home"))