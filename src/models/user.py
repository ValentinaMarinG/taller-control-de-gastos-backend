from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates 
import re

from src.database import db, ma

from src.models.income import Income
from src.models.outgo import Outgo


class User(db.Model):
    id           = db.Column(db.String(10), primary_key=True, unique=True)
    name         = db.Column(db.String(80), nullable=False)
    lastname     = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    email        = db.Column(db.String(60), unique=True, nullable=False)
    password     = db.Column(db.String(128), nullable=False)
    
    create_at   = db.Column(db.DateTime, default=datetime.now)
    update_at   = db.Column(db.DateTime, onupdate=datetime.now)

    incomes = db.relationship('Income', backref='owner')
    outgoes = db.relationship('Outgo', backref='owner')
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def __repr__(self) -> str:
        return f"User >>> {self.name}"
    
    def __setattr__(self, name, value):
        if(name == "password"):
            value = User.hash_password(value)
        
        super(User, self).__setattr__(name, value)
        
    @staticmethod
    def hash_password(password):
        if not password:
            raise AssertionError("Password not provided")
        
        if not re.match("^(?=.*\d)(?=.*[A-Z]).+$", password):
           raise AssertionError("Password must contain 1 capital letter and 1 number")
        
        if len(password) < 8 or len(password) > 50:
            raise AssertionError("Password must be between 8 and 50 characters")
        
        return generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @validates('id')
    def validate_id(self, key, value):
        if not value:
            raise AssertionError('No id provided')
        if not value.isalnum():
            raise AssertionError('Id value must be alphanumeric')
        if len(value) < 3 or len(value) > 10:
            raise AssertionError('Id must be between 3 and 10 characters')
        if User.query.filter(User.id == value).first():
            raise AssertionError('Id is already in use')
        return value 

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise AssertionError('No name provided')
        if not value.isalnum():
            raise AssertionError('Name value must be alphanumeric')
        if len(value) < 4 or len(value) > 80:
            raise AssertionError('Name must be between 5 and 80 characters') 
        return value
    
    @validates('lastname')
    def validate_lastname(self, key, value):
        if not value:
            raise AssertionError('No lastname provided')
        if not value.isalnum():
            raise AssertionError('Lastname value must be alphanumeric')
        if len(value) < 4 or len(value) > 80:
            raise AssertionError('Lastname must be between 5 and 80 characters') 
        return value
    
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not value:
            raise AssertionError('No phone number provided')
        if not value.isalnum():
            raise AssertionError('Phone number value must be alphanumeric')
        if len(value) == 9:
            raise AssertionError('Phone number must be of 10 characters') 
        return value
    
    @validates('email')
    def validate_email(self, key, value):
        if not value:
            raise AssertionError('No email provided')
        if not re.match("[^@]+@[^@]+\.[^@]+", value):
            raise AssertionError('Provided email is not an email address')
        if User.query.filter(User.email == value).first():
            raise AssertionError('Email is already in use')
        return value
    
    
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
user_schema = UserSchema()
users_schema = UserSchema(many=True)