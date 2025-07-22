from cost_core import create_app
from cost_core.extensions import db
from flask_migrate import Migrate, upgrade

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
