from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import ProdukKategori
from sqlalchemy import desc
import uuid
import hashlib
from blueprints import admin_required, seller_required, buyer_required
# from blueprints import internal_required

bp_produk_kategori = Blueprint('table_produk_kategori', __name__)
api = Api(bp_produk_kategori)


class ProdukKategoriResource(Resource):

    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json', required=True)

        args = parser.parse_args()

        hasil = ProdukKategori(args['nama'])
        db.session.add(hasil)
        db.session.commit()

        app.logger.debug('DEBUG: %s', hasil)

        return marshal(hasil, ProdukKategori.response_fields), 200

    def get(self, id):
        # ambil data dari database
        qry = ProdukKategori.query.get(id)

        if qry is not None:
            return marshal(qry, ProdukKategori.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'Not Found'}, 404, {'Content-Type': 'application/json'}

    @admin_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json')
        args = parser.parse_args()

        qry = ProdukKategori.query.get(id)
        if qry is None:
            return {'Status ': 'Not Found'}, 404

        qry.nama = args['nama']
        db.session.commit()

        return marshal(qry, ProdukKategori.response_fields), 200

    @admin_required
    def delete(self, id):

        qry = ProdukKategori.query.get(id)
        if qry is None:
            return {'status': 'Not Found'}, 404
        db.session.delete(qry)
        db.session.commit()

        return {'status': "Deleted"}, 200


class DaftarProdukKategori(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        args = parser.parse_args()

        offset = (args['p']*args['rp']-args['rp'])
        qry = ProdukKategori.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ProdukKategori.response_fields))

        return rows, 200


api.add_resource(DaftarProdukKategori, '', '/daftar')
api.add_resource(ProdukKategoriResource, '', '/<id>')
