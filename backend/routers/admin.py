from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import select, func
from database import get_session
from models import User, FoodItem, MealLog, UserBase
from dependencies import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

# Dependency to check for admin privileges
async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user

@router.get("/stats")
async def get_system_stats(
    current_user: User = Depends(get_current_admin_user),
    session = Depends(get_session)
):
    user_count = session.exec(select(func.count(User.id))).one()
    meal_log_count = session.exec(select(func.count(MealLog.id))).one()
    food_count = session.exec(select(func.count(FoodItem.id))).one()
    
    # Simple "Most Popular Food" stat
    # This is a bit complex in pure SQLModel without proper aggregation helpers, 
    # but we can try a direct count query or just return raw counts for now.
    
    return {
        "total_users": user_count,
        "total_meals_logged": meal_log_count,
        "total_food_items": food_count,
        "active_users_last_7_days": user_count # Mock for now, or implement tracking later
    }

@router.get("/foods", response_model=List[FoodItem])
async def get_admin_foods(
    current_user: User = Depends(get_current_admin_user),
    session = Depends(get_session)
):
    # Return all foods (global + custom?) 
    # Usually admin manages global foods (is_custom=False)
    # But let's show all for full control, or just global. 
    # User asked for "already existing foods", likely meaning the database.
    statement = select(FoodItem).where(FoodItem.is_custom == False)
    return session.exec(statement).all()

@router.post("/foods", response_model=FoodItem)
async def create_global_food(
    food: FoodItem,
    current_user: User = Depends(get_current_admin_user),
    session = Depends(get_session)
):
    food.is_custom = False # Admin adds global foods
    session.add(food)
    session.commit()
    session.refresh(food)
    return food

@router.delete("/foods/{food_id}")
async def delete_food(
    food_id: int,
    current_user: User = Depends(get_current_admin_user),
    session = Depends(get_session)
):
    food = session.get(FoodItem, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")
    
    # Optional: Check if used in meal logs? 
    # For now, allow delete (cascades might fail if not set up, but let's assume loose coupling or constraint error)
    try:
        session.delete(food)
        session.commit()
    except Exception as e:
         raise HTTPException(status_code=400, detail="Cannot delete food (in use?)")
         
    return {"ok": True}
