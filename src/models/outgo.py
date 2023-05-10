from datetime import datetime

from src.database import db, ma

class Outgo(db.Model):
    id           = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    date         = db.Column(db.DateTime, default=datetime.now())
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
        return f"Outgo >>> {self.id}"
    
class OutgoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Outgo
        include_fk = True
outgo_schema=OutgoSchema()
outgoes_schema=OutgoSchema(many=True)
