import json
import hashlib
import uuid
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Sellers
from blueprints import db, app
from sqlalchemy import desc
# from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required

bp_seller = Blueprint('seller', __name__)
api = Api(bp_seller)


class SellerResource(Resource):

    def post(self):
        claims = get_jwt_claims();
        if claims['status'] == 'seller':
            parser = reqparse.RequestParser()
            parser.add_argument('name', location='json', required=True)
            parser.add_argument('email', location='json', required=True)
            parser.add_argument('address', location='json')
            parser.add_argument('phone', location='json')
            parser.add_argument('bank_account', location='json')

            args = parser.parse_args()

            seller = Sellers(args['name'], args['email'], args['province'], args['city'], args['postal_code'], args['city_type'], args['street'],
                             args['phone'], args['bank_account'], claims['id'])

            db.session.add(seller)
            db.session.commit()
            app.logger.debug('DEBUG: %s', seller)

            return marshal(seller, Sellers.response_field), 200, {'Content-Type': 'application/json'}

    def patch(self):
        claims = get_jwt_claims();
        qry = Clients.query.get(claims['id'])
        if qry is None:
            return {'Status ': 'Not Found'}, 404
        else:
            if claims['status'] == 'seller':
                parser = reqparse.RequestParser()
                parser.add_argument('name', location='json')
                parser.add_argument('email', location='json')
                parser.add_argument('province', location='json', required=True)
                parser.add_argument('city', location='json', required=True)
                parser.add_argument('postal_code', location='json', required=True)
                parser.add_argument('city_type', location='json', required=True)
                parser.add_argument('street', location='json', required=True)
                parser.add_argument('phone', location='json')
                parser.add_argument('bank_account', location='json')
                args = parser.parse_args()
                
                qry.username = args['name']
                qry.username = args['email']
                qry.username = args['province']
                qry.username = args['city']
                qry.username = args['postal_code']
                qry.username = args['city_type']
                qry.username = args['street']
                qry.username = args['phone']
                qry.username = args['bank_account']
            
                db.session.commit()


                return marshal(qry, Sellers.response_fields), 200, {'Content-Type': 'application/json'}
       
    
    def get(self):
        claims = get_jwt_claims();
        if claims['status'] == 'seller':
            qry = Sellers.query.get(claims['id'])
            if qry is not None:
                return marshal(qry, Sellers.response_field), 200
            return {'status':'NOT_FOUND'}, 404

# Routes
api.add_resource(SellerResource, '/profile')
