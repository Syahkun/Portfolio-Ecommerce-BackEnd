import json
import hashlib
import uuid
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Pembeli
from blueprints import db, app
from sqlalchemy import desc
from ..pengguna.model import Pengguna
# from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from blueprints import admin_required, seller_required, buyer_required

bp_pembeli = Blueprint('table_pembeli', __name__)
api = Api(bp_pembeli)


class CustomerResource(Resource):

# hanya jika dia mempunyai status sebagai buyer
    @buyer_required
    def post(self):
        claims = get_jwt_claims();
        if claims['status'] == 'pembeli':
            parser = reqparse.RequestParser()
            parser.add_argument('nama', location='json', required=True)
            parser.add_argument('email', location='json', required=True)
            parser.add_argument('provinsi', location='json', required=True)
            parser.add_argument('kota', location='json', required=True)
            parser.add_argument('kode_pos', location='json', required=True)
            parser.add_argument('kota_type', location='json', required=True)
            parser.add_argument('street', location='json', required=True)
            parser.add_argument('phone', location='json')
            parser.add_argument('bod', location='json')

            args = parser.parse_args()

            hasil = Pembeli(
                args['nama'], args['email'], args['provinsi'], args['kota'], args['kode_pos'], args['kota_type'], args['street'], args['phone'], args['bod'], claims['id'])

            db.session.add(hasil)
            db.session.commit()
            app.logger.debug('DEBUG: %s', hasil)

            return marshal(hasil, Pembeli.response_field), 200

# hanya jika dia adalah client id itu sendiri
    @buyer_required
    def patch(self):
        claims = get_jwt_claims();
        qry = Pengguna.query.get(claims['id'])
        if qry is None:
            return {'Status ': 'Not Found'}, 404
        else:
            if claims['status'] == 'buyer':
                parser = reqparse.RequestParser()
                parser.add_argument('nama', location='json')
                parser.add_argument('email', location='json')
                parser.add_argument('provinsi', location='json', required=True)
                parser.add_argument('kota', location='json', required=True)
                parser.add_argument('kode_pos', location='json', required=True)
                parser.add_argument('kota_type', location='json', required=True)
                parser.add_argument('street', location='json', required=True)
                parser.add_argument('phone', location='json')
                parser.add_argument('bod', location='json')
                args = parser.parse_args()
                
                qry.nama_pengguna = args['nama']
                qry.nama_pengguna = args['email']
                qry.nama_pengguna = args['provinsi']
                qry.nama_pengguna = args['kota']
                qry.nama_pengguna = args['kode_pos']
                qry.nama_pengguna = args['kota_type']
                qry.nama_pengguna = args['street']
                qry.nama_pengguna = args['phone']
                qry.nama_pengguna = args['bod']
            
                db.session.commit()


                return marshal(qry, Pembeli.response_fields), 200, {'Content-Type': 'application/json'}
       
# hanya jika status dia sebagai buyer
    # @buyer_required
    @admin_required
    def get(self):
        claims = get_jwt_claims();
        if claims['status'] == 'buyer':
            qry = Pembeli.query.get(claims['id'])
            if qry is not None:
                return marshal(qry, Pembeli.response_field), 200
            return {'status':'NOT_FOUND'}, 404


api.add_resource(CustomerResource, '/profile')
