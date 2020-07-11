from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    # Create and define fields for parser
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    # @jwt_required
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)  # Return an item object
        except Exception as e:
            return {'message': 'An error occurs when getting the item.', 'error': e}, 500

        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exist".format(name)}, 400

        data = Item.parser.parse_args()  # Extract fields from request
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurs when inserting the item.'}, 500  # Internal server error

        access_token = create_access_token(identity='liam')
        return {'item': item.json(), 'token': access_token}, 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delte_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()  # Extract fields from request

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
