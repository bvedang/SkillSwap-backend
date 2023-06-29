from flask_restful import Resource, fields, marshal_with, reqparse
from app.models import User
from app import db
from werkzeug.security import generate_password_hash

user_fields = {
    'id': fields.Integer,
    'firstName': fields.String,
    'lastName': fields.String,
    'email': fields.String,
    'password_hash': fields.String,
}

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstName', type=str, required=True, help='First name is required.')
        parser.add_argument('lastName', type=str, required=True, help='Last name is required.')
        parser.add_argument('email', type=str, required=True, help='Email is required.')
        parser.add_argument('password', type=str, required=True, help='Password is required.')
        args = parser.parse_args()

        existing_user = User.query.filter_by(email=args['email']).first()
        if existing_user:
            return {'message': 'Email already exists.'}, 400

        user = User(firstName=args['firstName'], lastName=args['lastName'], email=args['email'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(user_fields)
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('firstName', type=str)
        parser.add_argument('lastName', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        if args['email'] and args['email'] != user.email:
            existing_user = User.query.filter_by(email=args['email']).first()
            if existing_user:
                return {'message': 'Email already exists.'}, 400

        user.firstName = args.get('firstName', user.firstName)
        user.lastName = args.get('lastName', user.lastName)
        user.email = args.get('email', user.email)
        if args.get('password'):
            user.password_hash = generate_password_hash(args['password'])
        db.session.commit()
        return user

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User {user_id} deleted successfully'}
