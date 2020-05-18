import json
import hashlib
import uuid
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Penjual
from blueprints import db, app
from sqlalchemy import desc
# from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from blueprints.pengguna.model import Pengguna
from blueprints import admin_required, seller_required, buyer_required

bp_penjual = Blueprint('table_penjual', __name__)
api = Api(bp_penjual)


class SellerResource(Resource):
    @seller_required
    def post(self):
        claims = get_jwt_claims()
        if claims['status'] == 'penjual':
            parser = reqparse.RequestParser()
            parser.add_argument('nama', location='json', required=True)
            parser.add_argument('email', location='json', required=True)
            parser.add_argument('provinsi', location='json')
            parser.add_argument('kota', location='json')
            parser.add_argument('kode_pos', location='json')
            parser.add_argument('kota_type', location='json')
            parser.add_argument('street', location='json')
            parser.add_argument('phone', location='json')
            parser.add_argument('bank_account', location='json')

            args = parser.parse_args()

            seller = Penjual(args['nama'], args['email'], args['provinsi'], args['kota'], args['kode_pos'], args['kota_type'], args['street'],
                             args['phone'], args['bank_account'], claims['id'])

            db.session.add(seller)
            db.session.commit()
            app.logger.debug('DEBUG: %s', seller)

            return marshal(seller, Penjual.response_field), 200, {'Content-Type': 'application/json'}

    @seller_required
    def patch(self):
        claims = get_jwt_claims()
        qry = Pengguna.query.get(claims['id'])
        if qry is None:
            return {'Status ': 'Not Found'}, 404
        else:
            if claims['status'] == 'penjual':
                parser = reqparse.RequestParser()
                parser.add_argument('nama', location='json')
                parser.add_argument('email', location='json')
                parser.add_argument('provinsi', location='json', required=True)
                parser.add_argument('kota', location='json', required=True)
                parser.add_argument('kode_pos', location='json', required=True)
                parser.add_argument(
                    'kota_type', location='json', required=True)
                parser.add_argument('street', location='json', required=True)
                parser.add_argument('phone', location='json')
                parser.add_argument('bank_account', location='json')
                args = parser.parse_args()

                qry.nama_pengguna = args['nama']
                qry.nama_pengguna = args['email']
                qry.nama_pengguna = args['provinsi']
                qry.nama_pengguna = args['kota']
                qry.nama_pengguna = args['kode_pos']
                qry.nama_pengguna = args['kota_type']
                qry.nama_pengguna = args['street']
                qry.nama_pengguna = args['phone']
                qry.nama_pengguna = args['bank_account']

                db.session.commit()

                return marshal(qry, Penjual.response_fields), 200, {'Content-Type': 'application/json'}

    @seller_required
    def get(self):
        claims = get_jwt_claims()
        qry = Penjual.query.filter_by(pengguna_id=claims['id']).first()
        if qry is not None:
            return marshal(qry, Penjual.response_field), 200
        return {'status': 'NOT_FOUND'}, 404


# Routes
api.add_resource(SellerResource, '/profile')
# api.add_resource(PenggunaResource, '', '/<id>')
