import json

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid

# create model classes here

# Many-to-Many relationships requires helper table
# According to the flask documentation
contacts = db.Table(
    "contacts",
    db.Column("contact_id", db.Integer, db.ForeignKey("contact.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True),
)
# Project Model


class Project(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    address = db.Column(db.String(256))
    city = db.Column(db.String(64))
    province = db.Column(db.String(64))
    postalCode = db.Column(db.String(64))
    neighbourhood = db.Column(db.String(256))
    year = db.Column(db.Integer)
    name = db.Column(db.String(64))
    type = db.Column(db.String(64))
    # one-to-many relationship to Note
    notes = db.relationship("Note", backref="project", lazy=True)
    contacts = db.relationship(
        "Contact",
        secondary=contacts,
        lazy="subquery",
        backref=db.backref("projects", lazy=True),
    )
