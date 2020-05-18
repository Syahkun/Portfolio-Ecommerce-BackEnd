from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Transaksi
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

bp_transaksi = Blueprint('table_transaksi', __name__)
api = Api(bp_transaksi)


class TransactionResource(Resource):

    @buyer_required
    def get(self):
        claims = get_jwt_claims()
        qry_pembeli = Pembeli.query.filter_by(pengguna_id=claims['id']).first()
        qry = Transaksi.query.filter_by(pembeli_id=qry_pembeli.id).first()
        if qry is not None:
            return marshal(qry, Transaksi.response_field), 200
        return {'status': 'NOT_FOUND'}, 404

    @buyer_required
    def post(self):  # menambah produk ke keranjang user
        parser = reqparse.RequestParser()
        parser.add_argument("produk_id", type=int, location="args")
        parser.add_argument("qty", type=int, location="args")
        parser.add_argument("shipping_method_id", type=int, location="args")
        parser.add_argument("payment_method_id", type=int, location="args")
        args = parser.parse_args()

        claims = get_jwt_claims()
        pembeli = Pembeli.query.filter_by(pengguna_id=claims['id']).first()
        pembeli_id = pembeli.id
        produk = Produk.query.get(args["produk_id"])

        if produk is None:
            return {"message": "Product Not Available"}, 404

        transaksi = Transaksi.query.filter_by(pembeli_id=pembeli_id).first()

        if transaksi is None:
            transaksi = Transaksi(
                pembeli_id, args['shipping_method_id'], args['payment_method_id'])
            db.session.add(transaksi)
            db.session.commit()

        td = TransaksiDetail(transaksi.id,
                             args["produk_id"], produk.harga, args["qty"])
        db.session.add(td)
        db.session.commit()

        transaksi.total_qty += args["qty"]

        # if transaksi.total_qty == "NULL" or transaksi.total_qty == "None" or transaksi.total_qty == "":
        #     transaksi.total_qty = int(args["qty"])
        # else:
        #     coba = transaksi.total_qty
        #     print(coba)
        #     print("=====================")
        #     transaksi.total_qty = int(coba) + args['qty']

        if produk.promo:
            transaksi.total_harga += (int(produk.harga) *
                                      ((100-int(produk.diskon))/100) * int(args['qty']))
        else:
            transaksi.total_harga += (int(produk.harga)*int(args["qty"]))

        transaksi.updated_at = datetime.now()
        db.session.commit()

        return {'status': 'Success'}, 200

    @buyer_required
    # @admin_required
    def delete(self, id):
        claims = get_jwt_claims()
        qry_buyer = Pembeli.query.filter_by(pengguna_id=claims['id']).first()
        print("==========================", qry_buyer)
        # qry_buyer_id = qry_buyer.query.get(id)
        qry_tran = Transaksi.query.get(id)
        qry = qry_tran.filter_by(pembeli_id=qry_buyer.id)
        print("==========================", qry)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'Trasactions DELETED'}, 200


api.add_resource(TransactionResource, '', '/<id>')
