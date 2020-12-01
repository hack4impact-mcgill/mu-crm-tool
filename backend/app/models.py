import json

from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

# create model classes here

# Donation Model
class Donation(db.Model):
    __tablename__ = "donations"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    donationSource = db.Column(db.String(128), nullable=False)
    event = db.Column(db.String(128))
    numTickets = db.Column(db.Integer)
    addedBy = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.user_id,
            "name": self.name,
            "email": self.email,
            "date": self.date,
            "donationSource": self.donationSource,
            "event": self.event,
            "numTickets": self.numTickets,
            "addedBy": self.addedBy,
        }

    @staticmethod
    def serialize_list(donations):
        json_donations = []
        for donation in donations:
            json_donations.append(donation.serialize)
        return json_donations

    def __repr__(self):
        return "<Donation %r>" % self.id


# Many-to-Many relationships requires helper table
# According to the flask documentation
contacts = db.Table(
    "contacts",
    db.Column(
        "contact_id",
        UUID(as_uuid=True),
        db.ForeignKey("contact.id"),
        primary_key=True,
        default=uuid.uuid4,
    ),
    db.Column(
        "project_id",
        UUID(as_uuid=True),
        db.ForeignKey("project.id"),
        primary_key=True,
        default=uuid.uuid4,
    ),
)
# Project Model


class Project(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
