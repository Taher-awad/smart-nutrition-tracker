from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import sys
from typing import List

from services.auth_service import AuthenticationService
from services.user_service import UserProfileService
from services.meal_service import MealService
from services.ai_service import AIEngine
from models import UserCreate, Token, User, UserUpdate, FoodItem, MealLog, WeeklyPlan, MealLogCreate

# Configure Loguru
logger.remove()
logger.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")
logger.add("logs/app.log", rotation="1 day", retention="7 days", level="DEBUG")

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Smart Nutrition Tracker API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency Injection
from dependencies import (
    get_auth_service, 
    get_user_service, 
    get_meal_service, 
    get_ai_service, 
    get_current_user,
    oauth2_scheme
)

logger.info("Application started")

@app.post("/token", response_model=Token)
# @limiter.limit("5/minute")
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    logger.info(f"Login attempt for: {form_data.username}")
    # auth_service.authenticate_user returns dict or None based on previous edit
    user_dict = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user_dict:
        logger.warning(f"Failed login attempt for: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(data={"sub": user_dict["email"]})
    logger.info(f"Successful login for: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=User, response_model_exclude={"hashed_password"})
# @limiter.limit("3/minute")
async def create_user(
    request: Request,
    user: UserCreate,
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    try:
        logger.info(f"Registration attempt for: {user.email}")
        if auth_service.user_repo.get_by_email(user.email):
            logger.warning(f"Registration failed - email exists: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Returns id (int)
        user_id = auth_service.register_user(user.dict(), user.password)
        
        # Fetch the created user
        created_user = auth_service.user_repo.find_by_id(user_id)
        
        logger.info(f"User registered successfully: {user.email}")
        return created_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.get("/users/me/", response_model=User, response_model_exclude={"hashed_password"})
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.put("/users/profile", response_model=User, response_model_exclude={"hashed_password"})
async def update_user_profile(
    profile: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserProfileService = Depends(get_user_service)
):
    updated_user = user_service.update_profile(current_user.id, profile.dict(exclude_unset=True))
    return updated_user

    return updated_user

# --- Admin Router ---
from routers import admin
app.include_router(admin.router)

# --- Food & Meal Endpoints ---

@app.on_event("startup")
def on_startup():
    from database import create_db_and_tables
    create_db_and_tables()
    
    # Seed Data
    from repositories.food_repository import FoodRepository
    food_repo = FoodRepository()
    # Deduplicate existing foods
    with food_repo.get_session() as session:
        from sqlmodel import select, col
        # Get all foods
        all_foods = session.exec(select(FoodItem)).all()
        seen_names = set()
        for food in all_foods:
            if food.name in seen_names:
                session.delete(food)
                logger.info(f"Removed duplicate food: {food.name}")
            else:
                seen_names.add(food.name)
        session.commit()

    # Seed Data safely
    if not food_repo.find_all():
         seed_data = [
            {"name": "Apple", "calories": 95, "protein": 0.5, "carbs": 25, "fats": 0.3, "is_custom": False},
            {"name": "Banana", "calories": 105, "protein": 1.3, "carbs": 27, "fats": 0.3, "is_custom": False},
            {"name": "Chicken Breast (100g)", "calories": 165, "protein": 31, "carbs": 0, "fats": 3.6, "is_custom": False},
            {"name": "Rice (1 cup cooked)", "calories": 205, "protein": 4.3, "carbs": 44.5, "fats": 0.4, "is_custom": False},
            {"name": "Egg (Large)", "calories": 78, "protein": 6, "carbs": 0.6, "fats": 5, "is_custom": False},
        ]
         with food_repo.get_session() as session:
             for item in seed_data:
                 # Check existence again just in case
                 exists = session.exec(select(FoodItem).where(FoodItem.name == item["name"])).first()
                 if not exists:
                     food_repo.insert_one(FoodItem(**item))
         logger.info("Seeded Food Database")
         
    logger.info("Database initialized (SQLite)")

@app.get("/foods", response_model=List[FoodItem])
async def get_foods(
    search: str = "",
    meal_service: MealService = Depends(get_meal_service)
):
    foods = meal_service.search_foods(search)
    return foods

@app.post("/foods", response_model=FoodItem)
async def create_custom_food(
    food: FoodItem,
    current_user: User = Depends(get_current_user),
    meal_service: MealService = Depends(get_meal_service)
):
    return meal_service.add_custom_food(food.dict())

@app.post("/meals", response_model=MealLog)
async def log_meal(
    meal: MealLogCreate,
    current_user: User = Depends(get_current_user),
    meal_service: MealService = Depends(get_meal_service)
):
    return meal_service.log_meal(current_user.id, meal.dict())

@app.get("/meals/history", response_model=List[MealLog])
async def get_meal_history(
    current_user: User = Depends(get_current_user),
    meal_service: MealService = Depends(get_meal_service)
):
    return meal_service.get_meal_history(current_user.id)

# --- AI & Planning Endpoints ---

@app.post("/ai/recognize", response_model=FoodItem)
async def recognize_food_image(
    current_user: User = Depends(get_current_user),
    ai_service: AIEngine = Depends(get_ai_service)
):
    return ai_service.recognize_image()

@app.post("/plans/generate", response_model=WeeklyPlan)
async def generate_meal_plan(
    current_user: User = Depends(get_current_user),
    ai_service: AIEngine = Depends(get_ai_service)
):
    return ai_service.generate_meal_plan(current_user.id)

@app.post("/plans/variations")
async def generate_meal_plan_variations(
    current_user: User = Depends(get_current_user),
    ai_service: AIEngine = Depends(get_ai_service)
):
    return ai_service.generate_meal_plan_variations(current_user.id)

@app.get("/analytics/summary")
async def get_analytics_summary(
    current_user: User = Depends(get_current_user),
    meal_service: MealService = Depends(get_meal_service)
):
    summary = meal_service.get_daily_summary(current_user.id)
    # Summary structure is {"today": {...}}
    # We need to add goal to "today" or top level?
    # Original: summary["goal"] = goal
    # Let's add it to the 'today' dict or keep it separate? 
    # Frontend expects { today: {.., goal: .. } } ??
    # Looking at original main.py, it was: summary["goal"] = user.goal
    # summary was just result of meal_service.get_daily_summary.
    # If meal_service returns {"today": ...}, then summary["goal"] works if summary is that dict.
    summary["goal"] = current_user.daily_calorie_goal or 2000
    return summary

@app.get("/")
async def root():
    return {"message": "Smart Nutrition Tracker API is running (SQLite Version)"}
