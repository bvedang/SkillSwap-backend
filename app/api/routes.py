from app import api
from app.api.resources.user.user_resourse import UserResource

api.add_resource(UserResource,"/user")
