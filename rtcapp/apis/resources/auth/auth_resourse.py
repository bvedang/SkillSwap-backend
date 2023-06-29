from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required
from rtcapp.models import User
from rtcapp import models

class AuthResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required.')
        parser.add_argument('password', type=str, required=True, help='Password is required.')
        args = parser.parse_args()

        email = args['email']
        password = args['password']

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {'message': 'Invalid email or password'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200