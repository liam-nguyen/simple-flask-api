from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegistration

app = Flask(__name__)

app.config['SECRET_KEY'] = 'jose'  # JWT Secret Key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Change the extension behavior but not the underlying behaviors
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

api = Api(app)
jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegistration, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    from db import db
    
    db.init_app(app)
    app.run(port=5000, debug=True)
