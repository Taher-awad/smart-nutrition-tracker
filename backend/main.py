from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from auth import create_access_token, get_current_user, get_password_hash, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_database
from models import UserCreate, Token, User, UserUpdate
from bson import ObjectId
from loguru import logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import sys

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

db = get_database()
logger.info("Application started")

@app.post("/token", response_model=Token)
@limiter.limit("5/minute")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Login attempt for: {form_data.username}")
    user = db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        logger.warning(f"Failed login attempt for: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    logger.info(f"Successful login for: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=User)
@limiter.limit("3/minute")
async def create_user(request: Request, user: UserCreate):
    try:
        logger.info(f"Registration attempt for: {user.email}")
        if db.users.find_one({"email": user.email}):
            logger.warning(f"Registration failed - email exists: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = get_password_hash(user.password)
        user_dict = user.dict()
        user_dict["hashed_password"] = hashed_password
        del user_dict["password"]
        
        result = db.users.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        logger.info(f"User registered successfully: {user.email}")
        return User(**user_dict)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}, user data: {user.dict() if hasattr(user, 'dict') else 'N/A'}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

def calculate_bmr_tdee(user: UserUpdate) -> float:
    # Mifflin-St Jeor Equation
    if user.gender.lower() == "male":
        bmr = (10 * user.weight) + (6.25 * user.height) - (5 * user.age) + 5
    else:
        bmr = (10 * user.weight) + (6.25 * user.height) - (5 * user.age) - 161
    
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    tdee = bmr * activity_multipliers.get(user.activity_level.lower(), 1.2)
    
    if user.goal == "lose":
        return tdee - 500
    elif user.goal == "gain":
        return tdee + 500
    return tdee

@app.put("/users/profile", response_model=User)
async def update_user_profile(profile: UserUpdate, current_user: User = Depends(get_current_user)):
    daily_calories = calculate_bmr_tdee(profile)
    
    update_data = profile.dict()
    update_data["daily_calorie_goal"] = daily_calories
    
    db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$set": update_data}
    )
    
    # Fetch updated user
    updated_user_data = db.users.find_one({"_id": ObjectId(current_user.id)})
    updated_user_data["id"] = str(updated_user_data["_id"])
    return User(**updated_user_data)

# --- Food & Meal Endpoints ---

from models import FoodItem, MealLog
from typing import List

@app.on_event("startup")
async def seed_food_database():
    if db.foods.count_documents({}) == 0:
        seed_data = [
            {"name": "Apple", "calories": 95, "protein": 0.5, "carbs": 25, "fats": 0.3, "is_custom": False},
            {"name": "Banana", "calories": 105, "protein": 1.3, "carbs": 27, "fats": 0.3, "is_custom": False},
            {"name": "Chicken Breast (100g)", "calories": 165, "protein": 31, "carbs": 0, "fats": 3.6, "is_custom": False},
            {"name": "Rice (1 cup cooked)", "calories": 205, "protein": 4.3, "carbs": 44.5, "fats": 0.4, "is_custom": False},
            {"name": "Egg (Large)", "calories": 78, "protein": 6, "carbs": 0.6, "fats": 5, "is_custom": False},
        ]
        db.foods.insert_many(seed_data)
        print("Seeded Food Database")

@app.get("/foods", response_model=List[FoodItem])
async def get_foods(search: str = ""):
    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    foods = list(db.foods.find(query))
    return foods

@app.post("/foods", response_model=FoodItem)
async def create_custom_food(food: FoodItem, current_user: User = Depends(get_current_user)):
    food.is_custom = True
    # Optionally link to user if private
    db.foods.insert_one(food.dict())
    return food

@app.post("/meals", response_model=MealLog)
async def log_meal(meal: MealLog, current_user: User = Depends(get_current_user)):
    meal.user_id = current_user.id
    db.meals.insert_one(meal.dict())
    return meal

@app.get("/meals/history", response_model=List[MealLog])
async def get_meal_history(current_user: User = Depends(get_current_user)):
    meals = list(db.meals.find({"user_id": current_user.id}))
    return meals

# --- AI & Planning Endpoints ---

from models import WeeklyPlan
import random
from datetime import datetime, timedelta

@app.post("/ai/recognize", response_model=FoodItem)
async def recognize_food_image(current_user: User = Depends(get_current_user)):
    # Mock AI: Returns a random food from DB or a fixed one
    foods = list(db.foods.find())
    if foods:
        recognized = random.choice(foods)
        # Ensure no _id in response if not handled by model
        if "_id" in recognized:
            del recognized["_id"]
        return FoodItem(**recognized)
    return FoodItem(name="Unknown Food", calories=0, protein=0, carbs=0, fats=0)

@app.post("/plans/generate", response_model=WeeklyPlan)
async def generate_meal_plan(current_user: User = Depends(get_current_user)):
    # Mock Planner: Generates a random plan for 7 days
    start_date = datetime.utcnow()
    meals = []
    foods = list(db.foods.find())
    
    if not foods:
        # Fallback if no foods
        foods = [{"name": "Apple", "calories": 95, "protein": 0.5, "carbs": 25, "fats": 0.3}]

    for i in range(7):
        day_date = start_date + timedelta(days=i)
        # 3 meals per day
        for meal_type in ["breakfast", "lunch", "dinner"]:
            food = random.choice(foods)
            if "_id" in food:
                del food["_id"]
            meals.append({
                "date": day_date,
                "meal_type": meal_type,
                "food": food
            })
            
    plan = WeeklyPlan(
        user_id=current_user.id,
        start_date=start_date,
        meals=meals
    )
    
    # Save plan (optional, or just return)
    # db.plans.insert_one(plan.dict())
    return plan

@app.get("/analytics/summary")
async def get_analytics_summary(current_user: User = Depends(get_current_user)):
    # Simple summary: Total calories today
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    logs = list(db.meals.find({
        "user_id": current_user.id,
        "date": {"$gte": today}
    }))
    
    total_calories = sum(log["food_item"]["calories"] for log in logs)
    total_protein = sum(log["food_item"]["protein"] for log in logs)
    total_carbs = sum(log["food_item"]["carbs"] for log in logs)
    total_fats = sum(log["food_item"]["fats"] for log in logs)
    
    return {
        "today": {
            "calories": total_calories,
            "protein": total_protein,
            "carbs": total_carbs,
            "fats": total_fats
        },
        "goal": current_user.daily_calorie_goal or 2000
    }

@app.get("/")
async def root():
    return {"message": "Smart Nutrition Tracker API is running"}
