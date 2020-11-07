from flask import Blueprint

mu_user = Blueprint("mu_user", __name__)

from . import routes
