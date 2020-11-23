import json

from . import db, http_auth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid
# create model classes here


#Authorization for User
@http_auth.verify_token
def verify_auth_token(token):
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False  # valid token, but expired
    except BadSignature:
        return False  # invalid token
    user = MuUser.query.get(data["token"])
    return user
#MuUser Domain Model Class
class MuUser(db.Model)    
    #Initializing Table
    __tablename__='users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), unique=True, nullable=False)
    #Relationships
    notes = db.relationship("Note", backref="user")
    donations = db.relationship("Donation", backref="user")
    #Password Properties
    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def change_password(self, old_password, new_password):
        if not self.verify_password(old_password):
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True
    def generate_auth_token(self, expiration=86400):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"token": self.id})
    #Serialize class
    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "password_hash": self.password_hash,
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
