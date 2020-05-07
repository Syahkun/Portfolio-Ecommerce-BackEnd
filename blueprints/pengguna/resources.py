from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import Pengguna
from sqlalchemy import desc
import uuid
import hashlib
# from blueprints import internal_required

bp_client = Blueprint('client', __name__)
api = Api(bp_client)


class PenggunaResource(Resource):

    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_pengguna', location='json', required=True)
        parser.add_argument('kata_kunci', location='json')
        parser.add_argument('status', location='json',
                            required=True, choices=('seller', 'buyer', 'admin'))
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['kata_kunci'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        result = Pengguna(args['nama_pengguna'], hash_pass, args['status'], salt)
        db.session.add(result)
        db.session.commit()

        app.logger.debug('DEBUG: %s', result)

        return marshal(result, Clients.response_fields), 200

    # @internal_required
    def get(self, id):
        qry = Clients.query.get(id)
        if qry is not None:
            return marshal(qry, Clients.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'id is gone'}, 404, {'Content-Type': 'application/json'}

    # @internal_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_pengguna', location='json')
        parser.add_argument('kata_kunci', location='json')
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['kata_kunci'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        qry = Clients.query.get(id)
        if qry is None:
            return {'Status ': 'Not Found'}, 404

        qry.nama_pengguna = args['nama_pengguna']
        qry.kata_kunci = hash_pass
        qry.salt = salt
        db.session.commit()

        return marshal(qry, Clients.response_fields), 200

    # @internal_required
    def delete(self, id):
        qry = Clients.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


class ClientList(Resource):
    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('status', location='args',
                            choices=('seller', 'buyer', 'admin'))

        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        qry = Clients.query

        #penyusunan berdasarkan tipe client (seller, buyer, & admin)
        if args['status'] is not None:
            qry = qry.filter_by(status=args['status'])


        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Clients.response_fields))

        return rows, 200


api.add_resource(ClientList, '', '/list')
api.add_resource(ClientResource, '', '/<id>')
