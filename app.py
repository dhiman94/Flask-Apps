from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import jwt_required, JWT
from security import authenticate_users, identity

app = Flask(__name__)
api = Api(app)
items = []
app.secret_key = 'dhiman'
jwt_token = JWT(app, authenticate_users, identity)  # will create '/auth' endpoint


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return ('message: name {} already exists'.format(name)), 400
        req_data = request.get_json()
        item = {'name': name,
                'price': req_data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}

    def put(self, name):
        req_data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': req_data['price']}
            items.append(item)
        else:
            item.update(req_data)
        return item


class Items(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=6000, debug=False)
