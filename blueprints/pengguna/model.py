from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship

class Pengguna(db.Model):
    __tablename__ = "table_pengguna"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_pengguna = db.Column(db.String(100), nullable=False, unique=True)
    kata_kunci = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    status = db.Column(db.String(30))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    # inisiasi hubungan fk table_pengguna ke seller dan customer
    customers = db.relationship('Customers', backref='table_pengguna', lazy=True)
    sellers = db.relationship('Sellers', backref='table_pengguna', lazy=True)
   
    # field yang akan ditampilkan
    response_fields ={
        'id' : fields.Integer,
        'nama_pengguna' : fields.String,
        'kata_kunci' : fields.String,
        'status' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
        }
    
    #disimpan di jwt nya dulu
    jwt_claims_fields = {
        'id' : fields.Integer,
        'nama_pengguna' : fields.String,
        'status' : fields.String
    }

    def __init__(self, nama_pengguna, kata_kunci, status, salt):
        self.nama_pengguna = nama_pengguna
        self.kata_kunci = kata_kunci
        self.status = status
        self.salt = salt
      

    def __repr__(self):
        return '<Client %r>'%self.id