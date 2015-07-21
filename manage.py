import os
from flask.ext.script import Manager

from flask.ext.migrate import Migrate, MigrateCommand
from fretaggregator.database import Base

from fretaggregator import app

manager = Manager(app)

class DB(object):
  def __init__(self, metadata):
    self.metadata = metadata
    
migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

@manager.command
def run():
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)
  
if __name__ == "__main__":
  manager.run()