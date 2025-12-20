from repositories.base import BaseRepository
from models import User
from typing import Optional

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.find_one(email=email)

    def create_user(self, user_data: dict) -> User:
        # Check if user already exists
        if self.get_by_email(user_data.get("email")):
            raise ValueError("User with this email already exists")
            
        user = User(**user_data)
        return self.insert_one(user)

    def update_user(self, user_id: int, update_data: dict) -> User:
        return self.update_one(user_id, update_data)
