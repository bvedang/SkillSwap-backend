from rtcapp import api
from rtcapp.apis.resources.user.user_resourse import UserResource, CreateUserResourse
from rtcapp.apis.resources.auth.auth_resourse import AuthResource

def init_routes():
    api.add_resource(CreateUserResourse, '/signup')
    api.add_resource(AuthResource, '/login')
    api.add_resource(UserResource, '/users/<int:user_id>')