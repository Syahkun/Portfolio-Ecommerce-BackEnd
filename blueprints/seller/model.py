from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from blueprints.client.model import Clients
from sqlalchemy import Integer, String, ForeignKey, Column


class Sellers(db.Model):
    __tablename__ = 'seller'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    provinsi = db.Column(db.String(30), nullable=False)
    kota = db.Column(db.String(30), nullable=False)
    postal_code = db.Column(db.String(30), nullable=False)
    kota_type = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15))
    bank_account = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    products = db.relationship('Products', backref="seller", lazy=True)

    response_field = {
        'id': fields.Integer,
        "client_id": fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'provinsi': fields.String,
        'kota': fields.String,
        'postal_code': fields.String,
        'kota_type': fields.String,
        'street': fields.String,
        'phone': fields.String,
        'bank_account': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime

    }

    def __init__(self, name, email, provinsi, kota, postal_code, kota_type, street, phone, bank_account, client_id):
        self.name = name
        self.email = email
        self.provinsi = provinsi
        self.kota = kota
        self.postal_code = postal_code
        self.kota_type = kota_type
        self.street = street
        self.phone = phone
        self.bank_account = bank_account
        self.client_id = client_id

    def __repr__(self):
        return '<Seller %r>' % self.id
