from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from blueprints.pengguna.model import Pengguna
from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import relationship


class Produk(db.Model):
    __tablename__ = 'table_produk'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(100), nullable=False)
    gambar = db.Column(db.String(255))
    gambar1 = db.Column(db.String(255))
    gambar2 = db.Column(db.String(255))
    gambar3 = db.Column(db.String(255))
    harga = db.Column(db.Integer, nullable=False)
    warna = db.Column(db.String(100))
    berat = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(10))
    stock = db.Column(db.Integer, nullable=False)
    promo = db.Column(db.Boolean, default=False)
    diskon = db.Column(db.Integer, default=0)
    deskripsi = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    produk_kategori_id = db.Column(
        db.Integer, db.ForeignKey('table_produk_kategori.id'))
    penjual_id = db.Column(db.Integer, db.ForeignKey('table_penjual.id'))
    gambar_produk = db.relationship(
        'GambarProduk', backref='table_produk', lazy=True)
    transaction_details = db.relationship(
        'TransaksiDetail', backref='table_produk', lazy=True)

    response_fields = {
        'id': fields.Integer,
        "produk_kategori_id": fields.Integer,
        "penjual_id": fields.Integer,
        'nama': fields.String,
        'gambar': fields.String,
        'gambar1': fields.String,
        'gambar2': fields.String,
        'gambar3': fields.String,
        "harga": fields.Integer,
        "warna": fields.String,
        'berat': fields.Integer,
        'size': fields.String,
        'stock': fields.Integer,
        'promo': fields.Boolean,
        'diskon': fields.Integer,
        'deskripsi': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime

    }

    def __init__(self, nama, gambar, gambar1, gambar2, gambar3, harga, warna, berat, size, stock, promo, diskon, deskripsi, produk_kategori_id, penjual_id):
        self.nama = nama
        self.gambar = gambar
        self.gambar1 = gambar1
        self.gambar2 = gambar2
        self.gambar3 = gambar3
        self.harga = harga
        self.warna = warna
        self.berat = berat
        self.size = size
        self.stock = stock
        self.promo = promo
        self.diskon = diskon
        self.deskripsi = deskripsi
        self.produk_kategori_id = produk_kategori_id
        self.penjual_id = penjual_id

    def __repr__(self):
        return '<Produk %r>' % self.id
