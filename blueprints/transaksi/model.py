from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from blueprints.pengguna.model import Pengguna
from sqlalchemy import Integer, String, ForeignKey, Column


class Transaksi(db.Model):
    __tablename__ = 'table_transaksi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_harga = db.Column(db.Integer, default=0)
    total_qty = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    pembeli_id = db.Column(db.Integer, db.ForeignKey('table_pembeli.id'))
    payment_method_id = db.Column(
        db.Integer, db.ForeignKey('payment_method.id'))
    shipping_method_id = db.Column(
        db.Integer, db.ForeignKey('shipping_method.id'))
    transaction_details = db.relationship(
        'TransaksiDetail', backref='table_transaksi', lazy=True)

    response_field = {
        'id': fields.Integer,
        "pembeli_id": fields.Integer,
        "payment_method_id": fields.Integer,
        "shipping_method_id": fields.Integer,
        "total_harga": fields.Integer,
        "total_qty": fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime

    }

    def __init__(self, pembeli_id, payment_method_id, shipping_method_id):
        self.pembeli_id = pembeli_id
        self.payment_method_id = payment_method_id
        self.shipping_method_id = shipping_method_id

    def __repr__(self):
        return '<Transaksi %r>' % self.id
