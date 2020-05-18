from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from .model import ReviewProduk
from sqlalchemy import desc
import uuid
import hashlib
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
# from blueprints import internal_required
from blueprints.transaksi.model import Transaksi
from blueprints.transaksi_detail.model import TransaksiDetail
from blueprints.produk_review.model import ReviewProduk
from blueprints.pembeli.model import Pembeli

from blueprints import admin_required, seller_required, buyer_required



bp_produk_review = Blueprint('table_review_produk', __name__)
api = Api(bp_produk_review)


class ProductReviewResource(Resource):

    @buyer_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gambar', location='json')
        parser.add_argument('review', location='json', required=True)
        # parser.add_argument('transaction_detail_id',
        #                     location='json', required=True)

        args = parser.parse_args()

        claims = get_jwt_claims()
        qry_customer = Pembeli.query.filter_by(
           pengguna_id=claims['id']).first()
        pembeli_id = qry_customer.id
        qry_transaction = Transaksi.query.filter_by(
            pembeli_id=pembeli_id).first()
        transac_id = qry_transaction.id
        qry_transacdetail = TransaksiDetail.query.filter_by(
            transactio_id=transac_id).first()
        transacdetail_id = qry_transacdetail.id

        hasil = ReviewProduk(
            args['gambar'], args['review'], transacdetail_id)
        db.session.add(hasil)
        db.session.commit()

        app.logger.debug('DEBUG: %s',  hasil)

        return marshal(hasil, ReviewProduk.response_fields), 200

    @admin_required
    @buyer_required
    def delete(self, id):

        qry = ReviewProduk.query.get(id)
        if qry is None:
            return {'status': 'Not Found'}, 404
        db.session.delete(qry)
        db.session.commit()

        return {'status': "Deleted"}, 200


class ProductReviewList(Resource):
    
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()

        offset = (args['p']*args['rp']-args['rp'])

        qry = qry.order_by(desc(ReviewProduk.created_at))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ReviewProduk.response_fields))

        return rows, 200


api.add_resource(ProductReviewList, '', '')
api.add_resource(ProductReviewResource, '', '/<id>')
