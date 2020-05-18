from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from blueprints.pengguna.model import Pengguna
from sqlalchemy import Integer, String, ForeignKey, Column


class TransaksiDetail(db.Model):
    __tablename__ = 'transaction_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('table_transaksi.id'))
    produk_id = db.Column(db.Integer, db.ForeignKey('table_produk.id'))
    harga = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    product_reviews = db.relationship(
        'ReviewProduk', backref='transaction_detail', lazy=True)

    response_field = {
        'id': fields.Integer,
        "pembeli_id": fields.Integer,
        "produk_id": fields.Integer,
        "harga": fields.Integer,
        "qty": fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime

    }

    def __init__(self, transaction_id, produk_id, harga, qty):
        self.transaction_id = transaction_id
        self.produk_id = produk_id
        self.harga = harga
        self.qty = qty

    def __repr__(self):
        return '<TransactionDetail %r>' % self.id
