from flask import render_template

from models import Submission
from fretaggregator import app
from .database import session

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