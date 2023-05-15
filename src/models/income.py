from datetime import datetime, time, date
from sqlalchemy.orm import validates

from src.database import db, ma

class Income(db.Model):
    id           = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    description  = db.Column(db.String(100), nullable=False)
    date         = db.Column(db.Date, nullable=False)
    hour         = db.Column(db.Time, nullable=True)
    value        = db.Column(db.Float, nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.now())
    updated_at   = db.Column(db.DateTime, onupdate=datetime.now())
    
    user_id      = db.Column(db.String(10),
                             db.ForeignKey('user.id',
                                           onupdate="CASCADE",
                                           ondelete="RESTRICT"),
                             nullable=False)
    
    def __init__(self, **fields):
        super().__init__(**fields)
        
    def __repr__(self) -> str:
        return f"Income >>> {self.id}"
    
    @validates('description')
    def validate_description(self, key, value):
        if not value:
            raise AssertionError('No description provided')
        return value
        
    @validates('date')
    def validate_date(self, key, value):
        fecha = datetime.strptime(value, '%Y-%m-%d').date()
        if not fecha:
            raise AssertionError('No date provided')
        if fecha > date.today():
            raise AssertionError('Date provided is not valid')
        return fecha
    
    @validates('hour')
    def validate_hour(self, key, value):
        hora = datetime.strptime(value, '%H:%M:%S').time()
        if not hora:
            raise AssertionError('No hour provided')
        if hora < time(0,0,0) or hora > time(23,59,59):
            raise AssertionError('Hour provided is not valid')
        return hora
    
    @validates('value')
    def validate_value(self, key, value):
        if not value:
            raise AssertionError('No value provided')
        if not value >= 0:
            raise AssertionError('The value provided must be positive')
        return value 
     
class IncomeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Income
        include_fk = True
income_schema=IncomeSchema()
incomes_schema=IncomeSchema(many=True)