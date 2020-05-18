from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship


class PaymentMethods(db.Model):
    __tablename__ = "payment_method"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    Transaksi = db.relationship(
        'Transaksi', backref='payment_method', lazy=True)

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
    }

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<PaymentMethod %r>' % self.id
