from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every item needs a store id.'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred while inserting the item.'}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete_from_db()
            except:
                return {'message': 'An error occurred while deleting the item.'}, 500
            return {'message': 'Item deleted'}, 200

        return {'message': "An item with name '{}' does not exist.".format(name)}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred while updating the item.'}, 500

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
