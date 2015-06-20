import os

from flask import Flask

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "fretaggregator.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import views
from . import filters

from database import Base, engine
Base.metadata.create_all(engine)