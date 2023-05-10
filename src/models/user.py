from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re

from src.database import db, ma

from src.models.income import Income
from src.models.outgo import Outgo

class User(db.Model):
    id           = db.Column(db.String(10), primary_key=True)
    name         = db.Column(db.String(80), nullable=False)
    lastname     = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    email        = db.Column(db.String(60), unique=True, nullable=False)
    password     = db.Column(db.String(128), nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.now())
    updated_at   = db.Column(db.DateTime, onupdate=datetime.now())

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
        
        #if not re.match("\d.*[A-Z]|[A-Z]. *\d", password):
        #   raise AssertionError("Password mut contain 1 capital letter and 1 number")
        
        if len(password) < 8 or len(password) > 50:
            raise AssertionError("Password must be between 8 and 50 characters")
        
        return generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
user_schema = UserSchema()
users_schema = UserSchema(many=True)