from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db
from .model import ProductTypes
from sqlalchemy import desc
import uuid
import hashlib
# from blueprints import internal_required

bp_product_type = Blueprint('product_type', __name__)
api = Api(bp_product_type)


class ProductTypeResource(Resource):

    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)

        args = parser.parse_args()

        hasil = ProductTypes(args['name'])
        db.session.add(hasil)
        db.session.commit()

        app.logger.debug('DEBUG: %s', customer)

        return marshal(hasil, ProductTypes.response_fields), 200

    def get(self, id):
        # ambil data dari database
        qry = ProductTypes.query.get(id)

        if qry is not None:
            return marshal(qry, ProductTypes.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'Not Found'}, 404, {'Content-Type': 'application/json'}

    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        args = parser.parse_args()

        qry = ProductTypes.query.get(id)
        if qry is None:
            return {'Status ': 'Not Found'}, 404

        qry.username = args['name']
        qry.password = hash_pass
        qry.salt = salt
        db.session.commit()

        return marshal(qry, ProductTypes.response_fields), 200

    def delete(self, id):

        qry = ProductTypes.query.get(id)
        if qry is None:
            return {'status': 'Not Found'}, 404
        db.session.delete(qry)
        db.session.commit()

        return {'status': "Deleted"}, 200


class ProductTypeList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        args = parser.parse_args()

        offset = (args['p']*args['rp']-args['rp'])
        qry = ProductTypes.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ProductTypes.response_fields))

        return rows, 200


api.add_resource(ProductTypeList, '', '/list')
api.add_resource(ProductTypeResource, '', '/<id>')
