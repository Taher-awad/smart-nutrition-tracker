from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from repositories.user_repository import UserRepository
from interfaces.services import IAuthenticationService
import os
from dotenv import load_dotenv

load_dotenv()

class AuthenticationService(IAuthenticationService):
    def __init__(self):
        self.user_repo = UserRepository()
        self.SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-for-development-only")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.ph = PasswordHasher()

    def verify_password(self, plain_password, hashed_password):
        try:
            self.ph.verify(hashed_password, plain_password)
            return True
        except VerifyMismatchError:
            return False

    def get_password_hash(self, password):
        return self.ph.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        # User is an object now, not a dict
        if not self.verify_password(password, user.hashed_password):
            return None
        # Convert to dict format expected by the rest of the app or return object
        # The main.py expects an object or dict, let's look at get_current_user in main.py
        # It calls find_by_email and returns User(**user_data). 
        # Since we return a User object here, we might need to adjust main.py.
        # Ideally, we return the user dictionary to be compatible with existing logic or refactor everything.
        # Given we changed models.py to SQLModel, User is a class.
        return user.dict()
    
    def register_user(self, user_data: Dict[str, Any], password: str) -> int:
        hashed_password = self.get_password_hash(password)
        user_data["hashed_password"] = hashed_password
        user = self.user_repo.create_user(user_data)
        return user.id
