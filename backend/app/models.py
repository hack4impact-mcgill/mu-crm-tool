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
    donation_source = db.Column(db.String(128), nullable=False)
    event = db.Column(db.String(128))
    num_tickets = db.Column(db.Integer)
    added_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "date": self.date,
            "donation_source": self.donation_source,
            "event": self.event,
            "num_tickets": self.num_tickets,
            "added_by": self.added_by,
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
    __tablename__ = "projects"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = db.Column(db.String(256))
    city = db.Column(db.String(64))
    province = db.Column(db.String(64))
    postal_code = db.Column(db.String(64))
    neighbourhood = db.Column(db.String(256))
    year = db.Column(db.Integer)
    name = db.Column(db.String(64))
    type = db.Column(db.String(64))
    contacts = db.relationship(
        "Contact",
        secondary=contacts,
        lazy="subquery",
        backref=db.backref("projects", lazy=True),
    )


# Contact Type Model
class ContactType(db.Model):
    __tablename__ = "contacttypes"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hex_colour = db.Column(db.String(8))
    type = db.Column(db.String(64))
    description = db.Column(db.String(512))
    contact = db.relationship("Contact", backref="ContactType", lazy=True)


# MuUser Domain Model Class
class MuUser(db.Model):
    # Initializing Table
    __tablename__ = "users"
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    role = db.Column(db.String(32), unique=True, nullable=False)
    donations = db.relationship("Donation", backref="user", lazy=True)
    # Serialize class
    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
        }

    @staticmethod
    def serialize_list(users):
        json_users = []
        for user in users:
            json_users.append(user.serialize)
        return json_users

    def __repr__(self):
        return "<User %r>" % self.email
