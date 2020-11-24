import json

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid
# create model classes here

# MuUser Domain Model Class
class MuUser(db.Model):   
    #Initializing Table
    __tablename__='users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), unique=True, nullable=False)
    #Relationships
    notes = db.relationship("Note", backref="user", lazy=True)
    donations = db.relationship("Donation", backref="user", lazy=True)
    #Serialize class
    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "password_hash": self.password_hash,
            "email": self.email,
            "role": self.role
        }
    @staticmethod
    def serialize_list(users):
        json_users = []
        for user in users:
            json_users.append(user.serialize)
        return json_users
    def __repr__(self):
        return "<User %r>" % self.email
