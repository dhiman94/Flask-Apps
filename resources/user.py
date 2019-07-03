from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help='This field can not be blank')
_user_parser.add_argument('password', type=str, required=True, help='This field can not be blank')


class UserRegister(Resource):
    def post(self):
        req_data = _user_parser.parse_args()
        if UserModel.find_by_username(req_data['username']):
            return {'message': 'user already exists'}, 400

        user = UserModel(req_data['username'], req_data['password'])
        user.save_to_db()

        return {'message': 'user registered successfully'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user with id {} not found'.format(user_id)}, 404
        user.delete_from_db()
        return {'message': 'user deleted'}, 200


class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.find_all()))}


class UserLogin(Resource):
    @classmethod
    def post(cls):
        req_data = _user_parser.parse_args()
        user = UserModel.find_by_username(req_data['username'])

        if user and safe_str_cmp(user.password, req_data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return {'message': 'invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access token': new_token}
