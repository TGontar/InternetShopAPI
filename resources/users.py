from flask_restful import reqparse, Resource, abort
from models.users import User
from db import db


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', required=True)

    def post(self):
        args = UserRegister.parser.parse_args()
        username = args['username']
        password = args['password']
        if User.find_by_username(username):
            abort(404, message=f"User {username} already exists")
        user = User(**args)
        user.post()
        return args