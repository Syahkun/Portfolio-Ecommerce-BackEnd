from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from blueprints.pengguna.model import Pengguna
from sqlalchemy import Integer, String, ForeignKey, Column


class Penjual(db.Model):
    __tablename__ = 'table_penjual'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    provinsi = db.Column(db.String(30), nullable=False)
    kota = db.Column(db.String(30), nullable=False)
    kode_pos = db.Column(db.String(30), nullable=False)
    kota_type = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15))
    bank_account = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    pengguna_id = db.Column(db.Integer, db.ForeignKey('table_pengguna.id'))
    produk = db.relationship('Produk', backref="table_penjual", lazy=True)

    response_field = {
        'id': fields.Integer,
        "pengguna_id": fields.Integer,
        'nama': fields.String,
        'email': fields.String,
        'provinsi': fields.String,
        'kota': fields.String,
        'kode_pos': fields.String,
        'kota_type': fields.String,
        'street': fields.String,
        'phone': fields.String,
        'bank_account': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime

    }

    def __init__(self, nama, email, provinsi, kota, kode_pos, kota_type, street, phone, bank_account,pengguna_id):
        self.nama = nama
        self.email = email
        self.provinsi = provinsi
        self.kota = kota
        self.kode_pos = kode_pos
        self.kota_type = kota_type
        self.street = street
        self.phone = phone
        self.bank_account = bank_account
        self.pengguna_id =pengguna_id

    def __repr__(self):
        return '<Penjual %r>' % self.id
