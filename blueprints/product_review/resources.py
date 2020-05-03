from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db
from .model import ProductReviews
from sqlalchemy import desc
import uuid
import hashlib
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
# from blueprints import internal_required
from blueprints.transaction.model import Transactions
from blueprints.transaction_detail.model import TransactionDetails
from blueprints.product_review.model import ProductReviews



bp_product_review = Blueprint('product_review', __name__)
api = Api(bp_product_review)


class ProductReviewResource(Resource):

    # cuma buyer doang
    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('picture', location='json')
        parser.add_argument('review', location='json', required=True)
        # parser.add_argument('transaction_detail_id',
        #                     location='json', required=True)

        args = parser.parse_args()

        claims = get_jwt_claims()
        qry_customer = Customers.query.filter_by(
            client_id=claims['id']).first()
        customer_id = qry_customer.id
        qry_transaction = Transactions.query.filter_by(
            customer_id=customer_id).first()
        transac_id = qry_transaction.id
        qry_transacdetail = TransactionDetails.query.filter_by(
            transactio_id=transac_id).first()
        transacdetail_id = qry_transacdetail.id

        hasil = ProductReviews(
            args['picture'], args['review'], transacdetail_id)
        db.session.add(hasil)
        db.session.commit()

        app.logger.debug('DEBUG: %s', product_review)

        return marshal(hasil, ProductReviews.response_fields), 200

    # for buyer and admin
    def delete(self, id):

        qry = ProductReviews.query.get(id)
        if qry is None:
            return {'status': 'Not Found'}, 404
        db.session.delete(qry)
        db.session.commit()

        return {'status': "Deleted"}, 200


class ProductReviewList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()

        offset = (args['p']*args['rp']-args['rp'])

        qry = qry.order_by(desc(ProductReviews.created_at))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ProductReviews.response_fields))

        return rows, 200


api.add_resource(ProductReviewList, '', '')
api.add_resource(ProductReviewResource, '', '/<id>')
