from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

import hashlib
import uuid
# from blueprints import internal_required
from ..pengguna.model import Pengguna

bp_login = Blueprint('login', __name__)
api = Api(bp_login)


class CreateTokenResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_pengguna', location='args', required=True)
        parser.add_argument('kata_kunci', location='args', required=True)
        args = parser.parse_args()

        qry_client = Pengguna.query.filter_by(
            nama_pengguna=args['nama_pengguna']).first()

        if qry_client is not None:
            client_salt = qry_client.salt
            status = qry_client.status
            encoded = ('%s%s' %
                       (args['kata_kunci'], client_salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()
            if hash_pass == qry_client.kata_kunci and qry_client.nama_pengguna == args['nama_pengguna']:
                qry_client = marshal(qry_client, Pengguna.jwt_claims_fields)
                qry_client['identifier'] = "asaacommerce"
                token = create_access_token(
                    identity=args['nama_pengguna'], user_claims=qry_client)
                return {'token': token, 'status': status}, 200
        return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 404


api.add_resource(CreateTokenResource, '')
