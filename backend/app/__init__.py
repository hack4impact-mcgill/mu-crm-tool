from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import config

# db = SQLAlchemy()
# migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    CORS(
        app,
        resources={
            r"/*": {"origins": [r"http://localhost:*", r"http://192.168.0.11:*"]}
        },
    )
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # call init_app to complete initialization
    # db.init_app(app)
    # migrate.init_app(app, db)

    # create app blueprints
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .contact import contact as contact_blueprint

    app.register_blueprint(contact_blueprint, url_prefix="/contact")

    from .contact_type import contact_type as contact_type_blueprint

    app.register_blueprint(contact_type_blueprint, url_prefix="/contact_type")

    from .donation import donation as donation_blueprint

    app.register_blueprint(donation_blueprint, url_prefix="/donation")

    from .mu_user import mu_user as mu_user_blueprint

    app.register_blueprint(mu_user_blueprint, url_prefix="/mu_user")

    from .note import note as note_blueprint

    app.register_blueprint(note_blueprint, url_prefix="/note")

    return app
