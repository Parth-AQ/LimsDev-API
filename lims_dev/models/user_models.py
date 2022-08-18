from db import db
import enum
from time import time
import jwt

class Roles(enum.Enum):
    super_admin = "super_admin"
    admin = "admin"

class UserModels(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80))
    role = db.Column(db.Enum(Roles))

    def __init__(self, first_name, last_name, email, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role

    def json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role.value
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_email_is_superadmin(cls, _id):
        return cls.query.filter_by(id=_id, role="super_admin").first()

    def save_to_db(self): # It can handle update and insert into the database
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_reset_token(cls, email, expires=500):
        return jwt.encode({'reset_password': email, 'exp': time() + expires}, key="TestLimsDev")

