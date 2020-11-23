import json

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
# create model classes here

class Donation(db.Model):
    __tablename__='donations'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    donationSource = db.Column(db.String(128), nullable=False)
    event = db.Column(db.String(128), nullable=False)
    numTickets = db.Column(db.Integer)
    addedBy = db.Column(db.Integer, db.ForeignKey('user.id')
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
            "addedBy": self.addedBy
        }
    @staticmethod
    def serialize_list(donations):
        json_donations = []
        for donation in donations:
            json_donations.append(donation.serialize)
        return json_donations
    def __repr__(self):
        return "<Donation %r>" % self.id
