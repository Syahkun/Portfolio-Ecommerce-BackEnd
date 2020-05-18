from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Produk
from blueprints import db, app
from blueprints.penjual.model import Penjual
from blueprints.produk_kategori.model import ProdukKategori
from sqlalchemy import desc
# from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from blueprints import admin_required, seller_required, buyer_required

bp_produk = Blueprint('table_produk', __name__)
api = Api(bp_produk)


class ProductResource(Resource):
    # @internal_required
    def get(self, id):
        qry = Produk.query.get(id)
        if qry is not None:
            return marshal(qry, Produk.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    # seller
    # @internal_required
    @seller_required
    # @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('gambar', location='json')
        parser.add_argument('gambar1', location='json')
        parser.add_argument('gambar2', location='json')
        parser.add_argument('gambar3', location='json')
        parser.add_argument('harga', location='json', required=True)
        parser.add_argument('warna', location='json')
        parser.add_argument('berat', location='json')
        parser.add_argument('size', location='json')
        parser.add_argument('stock', location='json')
        parser.add_argument('promo', location='json', type=bool)
        parser.add_argument('diskon', type=int, location='json')
        parser.add_argument('deskripsi', location='json')
        parser.add_argument('produk_kategori_id', location='json')
        # parser.add_argument('seller_id', location='json')

        args = parser.parse_args()
        claims = get_jwt_claims()
        pengguna_id = claims["id"]
        qry_seller = Penjual.query.filter_by(pengguna_id=claims['id']).first()
        seller_id = qry_seller.id

        product = Produk(args['nama'], args['gambar'], args['gambar1'], args['gambar2'], args['gambar3'], args['harga'], args['warna'],
                         args['berat'], args['size'], args['stock'], args['promo'], args['diskon'], args['deskripsi'], args['produk_kategori_id'], seller_id)

        db.session.add(product)
        db.session.commit()
        app.logger.debug('DEBUG: %s', product)

        return marshal(product, Produk.response_fields), 200, {'Content-Type': 'application/json'}

    @seller_required
    def patch(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('harga', location='json', required=True)
        parser.add_argument('warna', location='json')
        parser.add_argument('berat', location='json')
        parser.add_argument('size', location='json')
        parser.add_argument('stock', location='json')
        parser.add_argument('promo', location='json', type=bool)
        parser.add_argument('diskon', type=int, location='json')
        parser.add_argument('produk_kategori_id', location='json')
        args = parser.parse_args()

        claims = get_jwt_claims()
        qry_seller = Penjual.query.filter_by(pengguna_id=claims['id']).first()
        seller_id = qry_seller.id
        qry_product = Produk.query.filter_by(seller_id=seller_id).all()
        qry = qry_product.get(id)

        if qry is None:
            return {'Status ': 'Not Found'}, 404

        qry.nama = args['nama']
        qry.harga = args['harga']
        qry.warna = args['warna']
        qry.berat = args['berat']
        qry.size = args['size']
        qry.stock = args['stock']
        qry.promo = args['promo']
        qry.disko = args['diskon']
        qry.produk_kategori_id = args['produk_kategori_id']

        db.session.commit()

        return marshal(qry, Produk.response_fields), 200, {'Content-Type': 'application/json'}

    @seller_required
    # @admin_required
    def delete(self, id):
        claims = get_jwt_claims()
        qry_seller = Penjual.query.filter_by(pengguna_id=claims['id']).first()
        seller_id = qry_seller.id
        qry_product = Produk.query.filter_by(penjual_id=seller_id)
        qry = qry_product.filter_by(id=id).first()

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


class ProductList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=1000)
        parser.add_argument('nama', location='json')
        parser.add_argument('size', location='json')
        parser.add_argument('warna', location='json')
        parser.add_argument('harga', location='json')
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=(
            'nama', 'size', 'warna', 'harga'))
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p']*args['rp']-args['rp'])
        qry = Produk.query
        if args['nama'] is not None:
            qry = qry.filter_by(nama=args['nama'])

        if args['size'] is not None:
            qry = qry.filter_by(size=args['size'])

        if args['warna'] is not None:
            qry = qry.filter_by(warna=args['warna'])

        if args['harga'] is not None:
            qry = qry.filter_by(harga=args['harga'])

        if args['orderby'] is not None:
            if args['orderby'] == 'nama':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Produk.nama))
                else:
                    qry = qry.order_by(Produk.nama)
            elif args['orderby'] == 'size':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Produk.size))
                else:
                    qry = qry.order_by(Produk.size)
            elif args['orderby'] == 'warna':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Produk.warna))
                else:
                    qry = qry.order_by(Produk.warna)
            elif args['orderby'] == 'harga':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Produk.harga))
                else:
                    qry = qry.order_by(Produk.harga)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Produk.response_fields))

        return rows, 200


class ProductPromo(Resource):

    def get(self):  # mengambil data yang memiliki promo diskon
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('order_by', location='args',
                            help='invalid orderby value', choices=['harga', 'diskon'])

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        qry = Produk.query.filter_by(promo=True)
        qry = qry.filter_by(status=True)
        qry = qry.order_by(desc(Produk.created_at))
        if args['order_by'] is not None:
            if args['order_by'] == 'harga':
                qry = qry.order_by(Produk.harga)  # @internal_required
            elif args['order_by'] == 'diskon':
                qry = qry.order_by(Produk.diskon)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Produk.response_fields))

        return rows, 200


class ProductSearch(Resource):

    def get(self):  # mengambil data semua produk, filter by category dan subcategory
        parser = reqparse.RequestParser()
        parser.add_argument("keyword", location="args")
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('order_by', location='args',
                            help='invalid orderby value', choices=['harga', 'diskon'])

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        if args['keyword'] is not None:
            product = Produk.query.filter(Produk.nama.like("%"+args['keyword']+"%") |
                                          Produk.ProdukKategori.nama.like("%"+args['keyword']+"%") |
                                          Produk.size.like("%"+args['keyword']+"%")) | Produk.warna.like("%"+args['keyword']+"%")

        product = product.order_by(desc(Produk.created_at))
        if args['order_by'] is not None:
            if args['order_by'] == 'harga':
                product = product.order_by(Produk.harga)
            elif args['order_by'] == 'sold':
                product = product.order_by(desc(Produk.sold))

        rows = []
        for row in product.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Produk.response_fields))

        return rows, 200


# Routes
api.add_resource(ProductList, '', '')
api.add_resource(ProductResource, '', '/<id>')
api.add_resource(ProductPromo, '', '/promo')
api.add_resource(ProductSearch, '', '/search')
