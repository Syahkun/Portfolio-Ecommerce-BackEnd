from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship


class GambarProduk(db.Model):
    __tablename__ = "table_gambar_produk"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gambar = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    produk_id = db.Column(db.Integer, db.ForeignKey('table_produk.id'))

    response_fields = {
        'id': fields.Integer,
        'gambar': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'produk_id': fields.Integer
    }

    def __init__(self, gambar, produk_id):
        self.gambar = gambar
        self.produk_id = produk_id

    def __repr__(self):
        return '<GambarProduk %r>' % self.id
