import json

from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# create model classes here
import datetime
import uuid

class Note(db.Model):
    __tablename__ = "notes"
    note_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = db.Column(db.String(256), nullable=False)
    createdDateTime = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    updatedDateTime = db.Column(db.DateTime(), default=None, nullable=False)
    # many to one relationship to Project
    project_id = db.Column(UUID(as_uuid=True), db.Foreign_Key('project.id'), nullable=False)
    # many one to relationship to MuUser via created_by
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('muuser.id'), nullable=False)
