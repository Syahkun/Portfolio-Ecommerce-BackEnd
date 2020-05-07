from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import ShippingMethods
from sqlalchemy import desc
import uuid
import hashlib
# from blueprints import internal_required

bp_shipping_method = Blueprint('shipping_method', __name__)
api = Api(bp_shipping_method)


class ShippingMethodResource(Resource):
    # admin
    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('courier', location='json', required=True)

        args = parser.parse_args()

        shipping_method = ShippingMethods(args['courier'])
        db.session.add(shipping_method)
        db.session.commit()

        app.logger.debug('DEBUG: %s', shipping_method)

        return marshal(shipping_method, ShippingMethods.response_fields), 200

    # semua bisa
    # @internal_required
    def get(self, id=None):
        # ambil data dari database
        qry = ShippingMethods.query.get(id)

        if qry is not None:
            return marshal(qry, ShippingMethods.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'id is gone'}, 404, {'Content-Type': 'application/json'}

    # admin
    # @internal_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('courier', location='json')
        args = parser.parse_args()

        qry = ShippingMethods.query.get(id)
        if qry is None:
            return {'Status ': 'Not Found'}, 404

        qry.courier = args['courier']
        db.session.commit()

        return marshal(qry, ShippingMethods.response_fields), 200

    # admin
    # @internal_required
    def delete(self, id=None):
        if id is not None:
            qry = ShippingMethods.query.get(id)
            if qry is not None:
                db.session.delete(qry)
                db.session.commit()
                return 'Data telah terhapus', 200, {
                    'Content-Type': 'application/json'
                }
            else:
                return 'id is not found', 404, {
                    'Content-Type': 'application/json'
                }
        else:
            return 'id tidak masuk', 404, {
                'Content-Type': 'application/json'
            }


class ShippingMethodList(Resource):
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        qry = ShippingMethods.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ShippingMethods.response_fields))

        return rows, 200


api.add_resource(ShippingMethodList, '', '')
api.add_resource(ShippingMethodResource, '', '/<id>')
