from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from fretaggregator import app
from .models import Submission, Song, Band, Video, User, Guitarist, VideoGuitarist
from .database import session
from .helpers import get_one_or_create, get_video_id

@app.route("/", methods=["GET"])
def home():
  """ Main page of the site """
  # Get a list of the most recent submissions
  recent_submissions = session.query(Submission).order_by(Submission.submission_date.desc()).limit(5)
  return render_template("home.html",
                        recent_submissions=recent_submissions
                        )

  
@app.route("/search", methods=["GET"])
def search_get():
  """ Searches for submissions based on song or band name and returns a page with results """
  search = request.args.get("search")
  submissions = session.query(Submission).join(Song).join(Band)
  results = submissions.filter((Song.title.ilike("%{}%".format(search))) | (Band.name.ilike("%{}%".format(search)))).order_by(Band.name, Song.title).all()
  return render_template("search.html", results=results)
  
  
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
  video_id = get_video_id(request.form["url"])
  video = get_one_or_create(session, Video, video_id=video_id)
  session.add_all([band, song, video])
  
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
                          video=video,
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

@app.route("/details/<int:id>", methods=["GET"])
def details_get(id):
  """ Display page for a single submission """
  submission = session.query(Submission).get(id)
  return render_template("details.html", submission=submission)
  
@app.route("/learnmore", methods=["GET"])
def learn_more_get():
  """ Displays the Learn More About the Site page """
  return render_template("learnmore.html")