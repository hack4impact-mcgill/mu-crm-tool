import json
from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
from datetime import date
import random
import string


def random_bool():
    return random.choice([True, False])


def random_str(n):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))


def random_date():
    start = date.today().replace(day=1, month=1).toordinal()
    end = date.today().toordinal()
    return date.fromordinal(random.randint(start, end))


# create model classes here

# Donation Model
class Donation(db.Model):
    __tablename__ = "donations"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    donation_source = db.Column(db.String(128), nullable=False)
    event = db.Column(db.String(128))
    num_tickets = db.Column(db.Integer)
    added_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

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
            "amount": self.amount,
        }

    @staticmethod
    def serialize_list(donations):
        json_donations = []
        for donation in donations:
            json_donations.append(donation.serialize)
        return json_donations

    @staticmethod
    def populate(n=20):
        for _ in range(n):
            added_by = MuUser.random().id
            donation = Donation(
                name=random_str(64),
                email=random_str(64),
                date=random_date(),
                donation_source=random_str(128),
                event=random_str(128),
                num_tickets=random.randint(0, 1000),
                added_by=added_by,
                amount=random.randint(0, 1000),
            )
            db.session.add(donation)
        db.session.commit()

    def __repr__(self):
        return "<Donation %r>" % self.id


# Many-to-Many relationships requires helper table
# According to the flask documentation
association = db.Table(
    "association",
    db.Column(
        "contact_id",
        UUID(as_uuid=True),
        db.ForeignKey("contacts.id"),
        primary_key=True,
        default=uuid.uuid4,
    ),
    db.Column(
        "project_id",
        UUID(as_uuid=True),
        db.ForeignKey("projects.id"),
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
    is_completed = db.Column(db.Boolean, nullable=False)
    contacts = db.relationship(
        "Contact",
        secondary=association,
        lazy="subquery",
        backref=db.backref("project", lazy=True),
    )

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "address": self.address,
            "city": self.city,
            "province": self.province,
            "postal_code": self.postal_code,
            "neighbourhood": self.neighbourhood,
            "year": self.year,
            "name": self.name,
            "type": self.type,
            "contacts": Contact.serialize_list(self.contacts),
            "is_completed": self.is_completed,
        }

    @staticmethod
    def serialize_list(projects):
        json_projects = []
        for i in projects:
            json_projects.append(i.serialize)
        return json_projects

    @staticmethod
    def populate(n=20):
        for _ in range(n):
            project = Project(
                address=random_str(256),
                city=random_str(64),
                province=random_str(64),
                postal_code=random_str(64),
                neighbourhood=random_str(256),
                name=random_str(64),
                type=random_str(64),
                is_completed=random_bool(),
            )
            db.session.add(project)
        db.session.commit()

    def __repr__(self):
        return "<Project %r>" % self.id


belongs_to = db.Table(
    "belongs_to",
    db.Column(
        "contact_id",
        UUID(as_uuid=True),
        db.ForeignKey("contacts.id"),
        primary_key=True,
        default=uuid.uuid4,
    ),
    db.Column(
        "contact_type_id",
        UUID(as_uuid=True),
        db.ForeignKey("contact_types.id"),
        primary_key=True,
        default=uuid.uuid4,
    ),
)


# Contact Model
class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    secondary_email = db.Column(db.String(256))
    cellphone = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(256))
    organization = db.Column(db.String(256), nullable=False)
    neighbourhood = db.Column(db.String(256))
    # many to one realtionship with contact_type
    contact_types = db.relationship(
        "ContactType",
        secondary=belongs_to,
        lazy="subquery",
        backref=db.backref("contacts", lazy=True),
    )

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "secondary_email": self.secondary_email,
            "cellphone": self.cellphone,
            "role": self.role,
            "organization": self.organization,
            "neighbourhood": self.neighbourhood,
        }

    @staticmethod
    def serialize_list(contacts):
        json_contacts = []
        for c in contacts:
            json_contacts.append(c.serialize)
        return json_contacts

    @staticmethod
    def populate(n=20):
        for _ in range(n):
            contact = Contact(
                name=random_str(256),
                email=random_str(256),
                secondary_email=random_str(256),
                cellphone=random_str(256),
                role=random_str(256),
                organization=random_str(256),
                neighbourhood=random_str(256),
            )
            db.session.add(contact)
        db.session.commit()

    def __repr__(self):
        return "<Contact %r>" % self.id


# Contact Type Model
class ContactType(db.Model):
    __tablename__ = "contact_types"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hex_colour = db.Column(db.String(8))
    type = db.Column(db.String(64))
    description = db.Column(db.String(512))

    @property
    def serialize(self):
        return {
            "id": self.id,
            "hex_colour": self.hex_colour,
            "type": self.type,
            "description": self.description,
        }

    @staticmethod
    def serialize_list(contact_types):
        json_contact_types = []
        for contact_type in contact_types:
            json_contact_types.append(contact_type.serialize)
        return json_contact_types

    @staticmethod
    def populate(n=20):
        for _ in range(n):
            contact_type = ContactType(
                hex_colour=random_str(8),
                type=random_str(64),
                description=random_str(512),
            )
            db.session.add(contact_type)
        db.session.commit()


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

    @staticmethod
    def populate(n=20):
        for _ in range(n):
            user = MuUser(
                name=random_str(64), email=random_str(64), role=random_str(32)
            )
            db.session.add(user)
        db.session.commit()

    @staticmethod
    def random():
        users = MuUser.query.all()
        return random.choice(users)

    def __repr__(self):
        return "<User %r>" % self.email
