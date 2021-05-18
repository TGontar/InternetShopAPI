from flask_restful import reqparse, abort, Api, Resource
from flask_jwt import JWT, jwt_required, current_identity
from db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))

    def json(self):
        return {'username': self.username, 'password': self.password}

    @staticmethod
    def find_by_username(username):
        user = User.query.filter_by(username=username).first()
        return user

    @staticmethod
    def find_by_id(_id):
        user = User.query.filter_by(id=_id).first()
        return user

    def post(self):
        db.session.add(self)
        db.session.commit()