from sqlmodel import SQLModel, Field, JSON, Column
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import EmailStr

class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True)
    full_name: Optional[str] = None
    is_active: bool = True
    
    # Profile fields
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    activity_level: Optional[str] = None
    daily_calorie_goal: Optional[float] = None
    goal: Optional[str] = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_admin: bool = Field(default=False)

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    activity_level: Optional[str] = None
    goal: Optional[str] = None

class Token(SQLModel):
    access_token: str
    token_type: str

class FoodItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    calories: float
    protein: float
    carbs: float
    fats: float
    image_url: Optional[str] = None
    is_custom: bool = False
    details: Optional[Dict] = Field(default={}, sa_column=Column(JSON))

class MealLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    food_item_id: int = Field(foreign_key="fooditem.id")
    date: datetime
    meal_type: str # "breakfast", "lunch", "dinner", "snack"
    
    # Store snapshot of food in case it changes
    food_snapshot: Dict = Field(default={}, sa_column=Column(JSON))

class MealLogCreate(SQLModel):
    date: datetime
    meal_type: str
    food_item: Dict = {} 
    # Frontend sends 'food_item' dict. We will manually extract ID or create snapshot.


class WeeklyPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    start_date: datetime
    meals: List[Dict] = Field(default=[], sa_column=Column(JSON))

class MealPlanVariation(SQLModel):
    goal_name: str
    description: str
    meals: List[Dict]
    grocery_list: List[str]
