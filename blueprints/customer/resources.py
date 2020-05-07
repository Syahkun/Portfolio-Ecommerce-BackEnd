import json
import hashlib
import uuid
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Customers
from blueprints import db, app
from sqlalchemy import desc
from ..client.model import Clients 
# from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required

bp_customer = Blueprint('customer', __name__)
api = Api(bp_customer)


class CustomerResource(Resource):

# hanya jika dia mempunyai status sebagai buyer

    def post(self):
        claims = get_jwt_claims();
        if claims['status'] == 'buyer':
            parser = reqparse.RequestParser()
            parser.add_argument('name', location='json', required=True)
            parser.add_argument('email', location='json', required=True)
            parser.add_argument('provinsi', location='json', required=True)
            parser.add_argument('kota', location='json', required=True)
            parser.add_argument('postal_code', location='json', required=True)
            parser.add_argument('kota_type', location='json', required=True)
            parser.add_argument('street', location='json', required=True)
            parser.add_argument('phone', location='json')
            parser.add_argument('bod', location='json')

            args = parser.parse_args()

            customer = Customers(
                args['name'], args['email'], args['provinsi'], args['kota'], args['postal_code'], args['kota_type'], args['street'], args['phone'], args['bod'], claims['id'])

            db.session.add(customer)
            db.session.commit()
            app.logger.debug('DEBUG: %s', customer)

            return marshal(customer, Customers.response_field), 200, {'Content-Type': 'application/json'}

# hanya jika dia adalah client id itu sendiri

    def patch(self):
        claims = get_jwt_claims();
        qry = Clients.query.get(claims['id'])
        if qry is None:
            return {'Status ': 'Not Found'}, 404
        else:
            if claims['status'] == 'buyer':
                parser = reqparse.RequestParser()
                parser.add_argument('name', location='json')
                parser.add_argument('email', location='json')
                parser.add_argument('provinsi', location='json', required=True)
                parser.add_argument('kota', location='json', required=True)
                parser.add_argument('postal_code', location='json', required=True)
                parser.add_argument('kota_type', location='json', required=True)
                parser.add_argument('street', location='json', required=True)
                parser.add_argument('phone', location='json')
                parser.add_argument('bod', location='json')
                args = parser.parse_args()
                
                qry.nama_pengguna = args['name']
                qry.nama_pengguna = args['email']
                qry.nama_pengguna = args['provinsi']
                qry.nama_pengguna = args['kota']
                qry.nama_pengguna = args['postal_code']
                qry.nama_pengguna = args['kota_type']
                qry.nama_pengguna = args['street']
                qry.nama_pengguna = args['phone']
                qry.nama_pengguna = args['bod']
            
                db.session.commit()


                return marshal(qry, Customers.response_fields), 200, {'Content-Type': 'application/json'}
       
# hanya jika status dia sebagai buyer

    def get(self):
        claims = get_jwt_claims();
        if claims['status'] == 'buyer':
            qry = Customers.query.get(claims['id'])
            if qry is not None:
                return marshal(qry, Customers.response_field), 200
            return {'status':'NOT_FOUND'}, 404


api.add_resource(CustomerResource, '/profile')
