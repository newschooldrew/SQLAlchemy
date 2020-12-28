from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from db import db

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='this field cant be left blank')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404
        # next gives us the first item in this filter function
        # placing None in next(), gives the function a default

        # for item in items:
        #     if item['name'] == name:
        #         return item
        # return {'item': item}, 200 if item else 404

    def post(self, name):
        # if next(filter(lambda item: item['name'] == item, items), None):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        
        try:
            item.save_to_db()
        except:
            return {'messge':'an error occurred inserting the item'},500

        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        return {'items': list(map(lambda x: x.json(),items))}
