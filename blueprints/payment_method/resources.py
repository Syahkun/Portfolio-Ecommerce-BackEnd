from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import PaymentMethods
from sqlalchemy import desc
import uuid
import hashlib
# from blueprints import internal_required

bp_payment_method = Blueprint('payment_method', __name__)
api = Api(bp_payment_method)


class PaymentMethodResource(Resource):

    # untuk admin saja
    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        args = parser.parse_args()

        payment_method = PaymentMethods(
            args['name'])
        db.session.add(payment_method)
        db.session.commit()

        app.logger.debug('DEBUG: %s', payment_method)

        return marshal(payment_method, PaymentMethods.response_fields), 200

    # @internal_required
    def get(self, id=None):
        # ambil data dari database
        qry = PaymentMethods.query.get(id)

        if qry is not None:
            return marshal(qry, PaymentMethods.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'id is gone'}, 404, {'Content-Type': 'application/json'}

    # untuk admin
    # @internal_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_pengguna', location='json')
        parser.add_argument('kata_kunci', location='json')
        args = parser.parse_args()

        qry = PaymentMethods.query.get(id)
        if qry is None:
            return {'Status ': 'Not Found'}, 404

        qry.name = args['name']
        db.session.commit()

        return marshal(qry, PaymentMethods.response_fields), 200

    # untuk admin
    # @internal_required
    def delete(self, id=None):
        if id is not None:
            qry = PaymentMethods.query.get(id)
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


class PaymentMethodList(Resource):
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        qry = PaymentMethods.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, PaymentMethods.response_fields))

        return rows, 200


api.add_resource(PaymentMethodList, '', '')
api.add_resource(PaymentMethodResource, '', '/<id>')
