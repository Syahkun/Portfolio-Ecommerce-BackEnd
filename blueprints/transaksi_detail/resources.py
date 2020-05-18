from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import TransaksiDetail
from blueprints import db, app
from sqlalchemy import desc
# from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from blueprints.pembeli.model import Pembeli
from blueprints.produk.model import Produk
from blueprints.transaksi.model import Transaksi
from blueprints.transaksi_detail.model import TransaksiDetail
from datetime import datetime
from blueprints import admin_required, seller_required, buyer_required

bp_transaksi_detail = Blueprint('table_transaksi_detail', __name__)
api = Api(bp_transaksi_detail)


class TransaksiDetailRes(Resource):
    @buyer_required
    def get(self):
        claims = get_jwt_claims()

        qry_pembeli = Pembeli.query.filter_by(
            pengguna_id=claims['id']).first()
        qry_trans = Transaksi.query.filter_by(
            pembeli_id=qry_pembeli.id).first()
        qry = TransaksiDetail.query.filter_by(
            transaction_id=qry_trans.id).all()

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=100)
        args = parser.parse_args()

        offset = (args['p']*args['rp']-args['rp'])
        qry = Produk.query

        rows = []
        for row in qry:
            rows.append(marshal(row, TransaksiDetail.response_field))

        return rows, 200


api.add_resource(TransaksiDetailRes, '', '')
