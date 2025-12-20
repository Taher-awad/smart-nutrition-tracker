from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from services.auth_service import AuthenticationService
from services.user_service import UserProfileService
from services.meal_service import MealService
from services.ai_service import AIEngine
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_auth_service():
    return AuthenticationService()

def get_user_service():
    return UserProfileService()

def get_meal_service():
    return MealService()

def get_ai_service():
    return AIEngine()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_service.SECRET_KEY, algorithms=[auth_service.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # user is now a User object
    user = auth_service.user_repo.get_by_email(email)
    if user is None:
        raise credentials_exception
    
    return user
