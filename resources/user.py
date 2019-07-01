from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field can not be blank')
    parser.add_argument('password', type=str, required=True, help='This field can not be blank')

    def post(self):
        req_data = UserRegister.parser.parse_args()
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
