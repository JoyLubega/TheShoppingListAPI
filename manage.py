import os
from flask_script import Manager  # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from api import db, create_app

app = create_app(config_name='DevelopmentEnv')
MIGRATION_DIR = os.path.join('migrations')
migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()