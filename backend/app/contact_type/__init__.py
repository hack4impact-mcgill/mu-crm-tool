from flask import Blueprint

contact_type = Blueprint("contact_type", __name__)

from . import routes
