from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="username is required.")
    parser.add_argument('password', type=str, required=True, help="password is required.")

    def post(self):
        data = UserRegistration.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            access_token = create_access_token(identity=data['username'])
            return {'message': 'A user with this username is already existed!', 'token': access_token}, 400

        user = UserModel(**data)
        user.save_to_db()

        access_token = create_access_token(identity=data['username'])
        return {'message': 'User created successfully', 'token': access_token}, 201
