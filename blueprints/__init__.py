

import json
import config
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_script import Manager
from functools import wraps
from flask_cors import CORS, cross_origin


app = Flask(__name__)
jwt = JWTManager(app)
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)

@app.route("/")
def hello():
    return {"status": "OK"}, 200

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] != "admin":
            return {'status': 'FORBIDDEN', 'message': 'Khusus admin'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


def buyer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] != "pembeli":
            return {'status': 'FORBIDDEN', 'message': 'Hanya untuk pembeli'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


def seller_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] != "penjual":
            return {'status': 'FORBIDDEN', 'message': 'Hnaya untuk penjual'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


flask_env = os.environ.get('FLASK_ENV', 'Production')
if flask_env == "Production":
    app.config.from_object(config.ProductionConfig)
elif flask_env == "Testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.before_request
def before_request():
    if request.method != 'OPTIONS':  # <-- required
        pass
    else:
        # ternyata cors pake method options di awal buat ngecek CORS dan harus di return kosong 200, jadi di akalin gini deh. :D
        return {}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*'}


@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning("REQUEST_LOG\t%s",
                           json.dumps({
                               'method': request.method,
                               'code': response.status,
                               'uri': request.full_path,
                               'request': requestData,
                               'response': json.loads(response.data.decode('utf-8'))
                           })
                           )
    else:
        app.logger.error("REQUEST_LOG\t%s",
                         json.dumps({
                             'method': request.method,
                             'code': response.status,
                             'uri': request.full_path,
                             'request': requestData,
                             'response': json.loads(response.data.decode('utf-8'))
                         }))
    return response

from blueprints.transaksi_detail.resources import bp_transaksi_detail
from blueprints.pengguna.resources import bp_pengguna
from blueprints.transaksi.resources import bp_transaksi
from blueprints.shipping_method.resources import bp_shipping_method
from blueprints.penjual.resources import bp_penjual
from blueprints.produk_kategori.resources import bp_produk_kategori
from blueprints.produk_review.resources import bp_produk_review
from blueprints.produk.resources import bp_produk
from blueprints.gambar_produk.resources import bp_gambar_produk
from blueprints.payment_method.resources import bp_payment_method
from blueprints.login import bp_login
from blueprints.pembeli.resources import bp_pembeli

app.register_blueprint(bp_transaksi_detail, url_prefix='/transaksi_detail')
app.register_blueprint(bp_pengguna, url_prefix='/pengguna')
app.register_blueprint(bp_pembeli, url_prefix='/pembeli')
app.register_blueprint(bp_login, url_prefix='/login')
app.register_blueprint(bp_payment_method, url_prefix='/payment_method')
app.register_blueprint(bp_gambar_produk, url_prefix='/gambar_produk')
app.register_blueprint(bp_produk, url_prefix='/produk')
app.register_blueprint(bp_produk_review, url_prefix='/produk_review')
app.register_blueprint(bp_produk_kategori, url_prefix='/produk_kategori')
app.register_blueprint(bp_penjual, url_prefix='/penjual')
app.register_blueprint(bp_shipping_method, url_prefix='/shipping_method')
app.register_blueprint(bp_transaksi, url_prefix='/keranjang')

db.create_all()
