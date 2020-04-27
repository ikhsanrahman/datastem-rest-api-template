from app.services.service import BaseService
from app.models.user import User

class UserService(BaseService):
    pass

user_service = UserService(User)
