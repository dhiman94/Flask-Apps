from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserList, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, Items
from resources.store import Store, StoreList
from blacklist import BLACKLIST

# declare all the required configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFIACTIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)
app.secret_key = 'dhiman'
jwt = JWTManager(app)


# create all the tables in database
@app.before_first_request
def create_table():
    db.create_all()


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            'description': 'Token has expired',
            'error': 'token expired'
        }
    ), 401


@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify(
        {
            'description': 'Signature authorization failed',
            'error': 'invalid token'
        }
    ), 401


@jwt.unauthorized_loader
def missing_token_callback():
    return jsonify(
        {
            'description': 'token is missing',
            'error': 'missing token'
        }
    ), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify(
        {
            'description': 'The token is not fresh',
            'error': 'fresh token required'
        }
    ), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify(
        {
            'description': 'The token has been revoked',
            'error': 'token revoked'
        }
    ), 401


@jwt.token_in_blacklist_loader
def check_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


# add all the endpoints
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=6000, debug=False)
