from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import GambarProduk
from sqlalchemy import desc
import uuid
import hashlib
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from ..penjual.model import Penjual 
from ..gambar_produk.model import GambarProduk
from ..produk.model import Produk
from blueprints import seller_required
# from blueprints import internal_required

bp_gambar_produk = Blueprint('gambar_produk', __name__)
api = Api(bp_gambar_produk)


class GambarProdukResource(Resource):

    @seller_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gambar', location='json', required=True)
        parser.add_argument('produk_id', location='json', required=True)
        args = parser.parse_args()

        claims = get_jwt_claims()
        qry_seller = Penjual.query.filter_by(pengguna_id=claims['id']).first()
        seller_id = qry_seller.id
        qry_product = Produk.query.filter_by(seller_id=seller_id).all()
        qry_produk_id = qry_product.filter_by(id=args['produk_id']).first()
        qry_pic = qry_produk_id.id

        if qry_pic is None:
            return {'status': 'Produknya Mana?/Not found'}, 404

        gambar_produk = GambarProduk(args['gambar'], qry_pic)
        db.session.add(gambar_produk)
        db.session.commit()

        app.logger.debug('DEBUG: %s', gambar_produk)

        return marshal(gambar_produk, GambarProduk.response_fields), 200

    def get(self, id):
        # ambil data dari database
        qry = GambarProduk.query.get(id)

        if qry is not None:
            return marshal(qry, GambarProduk.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'Not Found'}, 404, {'Content-Type': 'application/json'}


class DaftarGambarProduk(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('produk_id', location='args')
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p']*args['rp']-args['rp'])
        qry = GambarProduk.query.filter_by(produk_id=args['produk_id'])

        if args['sort'] == 'desc':
            qry = qry.order_by(desc(GambarProduk.produk_id))
        else:
            qry = qry.order_by(GambarProduk.produk_id)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, GambarProduk.response_fields))

        return rows, 200


api.add_resource(DaftarGambarProduk, '', '/daftar_gambar_produk')
api.add_resource(GambarProdukResource, '', '/<id>')
