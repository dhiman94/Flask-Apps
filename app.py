from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate_users, identity
from resources.user import UserRegister, User, UserList
from resources.item import Item, Items
from resources.store import Store, StoreList

# declare all the required configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFIACTIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
app.secret_key = 'dhiman'
jwt_token = JWT(app, authenticate_users, identity)  # will create '/auth' endpoint


# create all the tables in database
@app.before_first_request
def create_table():
    db.create_all()


# add all the resources
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=6000, debug=False)
