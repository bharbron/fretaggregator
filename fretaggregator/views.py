from flask import render_template

import models
from fretaggregator import app
from .database import session

@app.route("/", methods=["GET"])
def home():
  return render_template("home.html")

@app.route("/results", methods=["GET"])
def results():
  pass
  #return render_template("results.html")