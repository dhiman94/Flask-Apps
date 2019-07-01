from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float, required=True,
        help="This field can't be blank"
    )
    parser.add_argument(
        'store_id', type=int, required=True,
        help="This field can't be blank"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json(), 201
        return {'message': 'item not found'}, 400

    def post(self, name):
        req_data = Item.parser.parse_args()
        if ItemModel.find_item_by_name(name):
            return {"message": "an item with name {} already exists".format(name)}, 401

        item = ItemModel(name, **req_data)

        try:
            item.save_to_db()
        except:
            return {'message': 'an error occurred while inserting the item'}, 500

        return item.json(), 200

    def delete(self, name):
        if ItemModel.find_item_by_name(name) is None:
            return {'message': 'item {} does not exist'.format(name)}

        item = ItemModel.find_item_by_name(name)
        item.delete()
        return {'message': 'item deleted'}

    def put(self, name):
        req_data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)

        if item is None:
            item = ItemModel(name, **req_data)
        else:
            item.price = req_data['price']
        item.save_to_db()
        return item.json(), 200


class Items(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

