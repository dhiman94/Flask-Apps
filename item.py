from flask_restful import Resource, reqparse
from flask import request
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float, required=True,
        help="This field can't be blank"
    )

    @classmethod
    def find_item_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @jwt_required()
    def get(self, name):
        item = Item.find_item_by_name(name)
        if item:
            return {'item': item}, 201
        return {'message': 'item not found'}, 400

    def post(self, name):
        req_data = Item.parser.parse_args()
        if Item.find_item_by_name(name):
            return {"message": "an item with name {} already exists".format(name)}, 401

        item = {'name': name, 'price': req_data['price']}

        try:
            Item.insert(item)
        except:
            return {'message': 'an error occurred while inserting the item'}, 500

        return item, 200

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()
        return {'message:': 'item inserted successfully'}

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

    def delete(self, name):
        if Item.find_item_by_name(name) is None:
            return {'message': 'item {} does not exist'.format(name)}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': 'item deleted'}

    def put(self, name):
        req_data = Item.parser.parse_args()
        item = Item.find_item_by_name(name)
        updated_item = {'name': name, 'price': req_data['price']}

        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {'message': 'an error occurred while inserting the item'}, 500
        else:
            Item.update(updated_item)
        return updated_item, 200


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        if items:
            return {'items': items}, 201
        else:
            return {'no item inserted'}, 400

