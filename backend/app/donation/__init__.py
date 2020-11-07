from flask import Blueprint

donation = Blueprint("donation", __name__)

from . import routes
