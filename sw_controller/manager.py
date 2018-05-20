import os
import sys
from flask_script import Manager

from app import create_app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])
manager = Manager(app)


if __name__ == '__main__':
    manager.run()
