from repositories.base import BaseRepository
from models import MealLog
from typing import List, Dict
from datetime import datetime
from sqlmodel import select, col

class MealRepository(BaseRepository[MealLog]):
    def __init__(self):
        super().__init__(MealLog)

    def log_meal(self, user_id: int, meal_data: dict) -> MealLog:
        # Ensure user_id is set
        meal_data["user_id"] = user_id
        meal = MealLog(**meal_data)
        return self.insert_one(meal)

    def get_history(self, user_id: int, limit: int = 50) -> List[MealLog]:
        with self.get_session() as session:
            statement = select(MealLog).where(MealLog.user_id == user_id).order_by(col(MealLog.date).desc()).limit(limit)
            return session.exec(statement).all()

    def get_daily_summary(self, user_id: int, date: datetime = None) -> Dict:
        if date is None:
            date = datetime.now()
        
        # Simple date filtering (could be improved with exact date ranges)
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)

        with self.get_session() as session:
            statement = select(MealLog).where(
                MealLog.user_id == user_id,
                MealLog.date >= start_of_day,
                MealLog.date <= end_of_day
            )
            meals = session.exec(statement).all()
        
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fats = 0

        for meal in meals:
            # Assuming food_snapshot or linked food_item has these details
            # For now, we will assume the meal log has a food_snapshot or we fetch from food_item
            # But the model has `food_snapshot`, let's rely on that if populated, or query the food item
            # To simplify, we'll assume `food_snapshot` is populated during logging
            food = meal.food_snapshot
            if food:
                total_calories += food.get("calories", 0)
                total_protein += food.get("protein", 0)
                total_carbs += food.get("carbs", 0)
                total_fats += food.get("fats", 0)
        
        return {
            "calories": total_calories,
            "protein": total_protein,
            "carbs": total_carbs,
            "fats": total_fats,
            "meals_count": len(meals)
        }
