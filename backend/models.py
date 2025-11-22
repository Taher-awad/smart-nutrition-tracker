from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    age: int = Field(ge=1, le=120, description="Age in years")
    gender: str = Field(pattern="^(male|female)$", description="Gender")
    height: float = Field(ge=50, le=300, description="Height in cm")
    weight: float = Field(ge=20, le=500, description="Weight in kg")
    activity_level: str = Field(pattern="^(sedentary|light|moderate|active|very_active)$")
    goal: str = Field(pattern="^(lose|maintain|gain)$")

class UserInDB(UserBase):
    hashed_password: str
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    activity_level: Optional[str] = None
    daily_calorie_goal: Optional[float] = None

class User(UserBase):
    id: str
    is_active: bool = True
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    activity_level: Optional[str] = None
    daily_calorie_goal: Optional[float] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class FoodItem(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fats: float
    image_url: Optional[str] = None
    is_custom: bool = False

class MealLog(BaseModel):
    user_id: str
    food_item: FoodItem
    date: datetime
    meal_type: str # "breakfast", "lunch", "dinner", "snack"

class WeeklyPlan(BaseModel):
    user_id: str
    start_date: datetime
    meals: List[dict] # Simplified for now
