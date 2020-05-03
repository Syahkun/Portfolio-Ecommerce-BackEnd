from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db
from .model import PicProducts
from sqlalchemy import desc
import uuid
import hashlib
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from ..seller.model import Sellers 
from ..pic_product.model import PicProducts
from ..product.model import Products
# from blueprints import internal_required

bp_pic_product = Blueprint('pic_product', __name__)
api = Api(bp_pic_product)


class PicProductResource(Resource):

    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('picture', location='json', required=True)
        parser.add_argument('product_id', location='json', required=True)
        args = parser.parse_args()

        claims = get_jwt_claims()
        qry_seller = Sellers.query.filter_by(client_id=claims['id']).first()
        seller_id = qry_seller.id
        qry_product = Products.query.filter_by(seller_id=seller_id).all()
        qry_product_id = qry_product.filter_by(id=args['product_id']).first()
        qry_pic = qry_product_id.id

        if qry_pic is None:
            return {'status': 'Produknya Mana?/Not found'}, 404

        pic_product = PicProducts(args['picture'], qry_pic)
        db.session.add(pic_product)
        db.session.commit()

        app.logger.debug('DEBUG: %s', pic_product)

        return marshal(pic_product, PicProducts.response_fields), 200

    def get(self, id):
        # ambil data dari database
        qry = PicProducts.query.get(id)

        if qry is not None:
            return marshal(qry, PicProducts.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'Not Found'}, 404, {'Content-Type': 'application/json'}


class PicProductList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('product_id', location='args')
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p']*args['rp']-args['rp'])
        qry = PicProducts.query.filter_by(product_id=args['product_id'])

        if args['sort'] == 'desc':
            qry = qry.order_by(desc(PicProducts.product_id))
        else:
            qry = qry.order_by(PicProducts.product_id)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, PicProducts.response_fields))

        return rows, 200


api.add_resource(PicProductList, '', '')
api.add_resource(PicProductResource, '', '/<id>')
