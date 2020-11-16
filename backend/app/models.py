import json

from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# create model classes here
import datetime

class Note(db.Model):
    __tablename__ = "notes"
    note_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)
    createdDateTime = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedDateTime = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    # many to one relationship to Project
    project_id = db.relationship(db.Integer, db.Foreign_Key('project.id'), nullable=False)
    # many one to relationship to MuUser via created_by
    created_by = db.relationship(db.Integer, db.Foreign_Key('muuser.id'), nullable=False)
