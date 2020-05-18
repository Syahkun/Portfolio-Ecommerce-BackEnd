from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship


class ProdukKategori(db.Model):
    __tablename__ = "table_produk_kategori"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    products = db.relationship('Produk', backref="table_produk_kategori", lazy=True)

    response_fields = {
        'id': fields.Integer,
        'nama': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, nama):
        self.nama = nama

    def __repr__(self):
        return '<ProdukKategori %r>' % self.id
