from flask_script import Manager  # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from api import db, create_app

app = create_app(config_name='DevelopmentEnv')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()