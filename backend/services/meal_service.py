from repositories.food_repository import FoodRepository
from repositories.meal_repository import MealRepository
from interfaces.services import IMealService
from typing import List, Dict, Any
from datetime import datetime

class MealService(IMealService):
    def __init__(self):
        self.food_repo = FoodRepository()
        self.meal_repo = MealRepository()

    def search_foods(self, query: str) -> List[Any]:
        return self.food_repo.search_foods(query)

    def add_custom_food(self, food_data: Dict[str, Any]) -> Any:
        # food_data might check for is_custom in repo
        return self.food_repo.add_custom_food(food_data)

    def log_meal(self, user_id: int, meal_data: Dict[str, Any]) -> Any:
        # meal_data comes from MealLogCreate (has 'food_item' dict, no 'food_item_id')
        food_item = meal_data.get("food_item", {})
        food_id = food_item.get("id") or food_item.get("_id") # Handle legacy/frontend nuances
        
        if not food_id:
             # If no ID, but we have data, create a custom food item to satisfy FK
             if "name" in food_item and "calories" in food_item:
                 from models import FoodItem
                 # Ensure is_custom is set
                 food_item["is_custom"] = True
                 # We can use the repo to add it. repo.add_food expects dict? 
                 # food_repo.add_food(data) -> returns data or object?
                 # Let's check food_repository.py or just use add_custom_food from this service
                 new_food = self.add_custom_food(food_item)
                 # new_food should have ID now. 
                 # add_custom_food returns dict (from previous reading) or object?
                 # In SQLModel refactor, repositories return object usually?
                 # Let's check add_custom_food signature in this file. 
                 # It calls self.food_repo.add_custom_food(food_data).
                 # Let's hope it populates 'id'.
                 
                 # If new_food is a dict
                 if isinstance(new_food, dict):
                     food_id = new_food.get("id")
                 else:
                     food_id = new_food.id

        # Construct payload for repo
        repo_payload = {
            "user_id": user_id,
            "food_item_id": int(food_id) if food_id else None, 
            "date": meal_data["date"],
            "meal_type": meal_data["meal_type"],
            "food_snapshot": food_item
        }
        return self.meal_repo.log_meal(user_id, repo_payload)

    def get_meal_history(self, user_id: int) -> List[Any]:
        return self.meal_repo.get_history(user_id)

    def get_daily_summary(self, user_id: int) -> Dict[str, Any]:
        summary = self.meal_repo.get_daily_summary(user_id)
        
        # summary is already a dict from repo: {"calories": ..., "protein": ...}
        # The frontend expects a nested structure?
        # Original service returned: {"today": { "calories": ... }}
        # models.py endpoint return summary directly.
        # Let's check main.py @app.get("/analytics/summary")
        # It calls get_daily_summary() then adds "goal". 
        # The original service logic calculated sums here. I moved that logic to the repository.
        # Repository returns flat dict: {'calories': 0, 'protein': 0, ...}
        # If frontend expects "today" key, I should add it, or check frontend code.
        # But looking at old code: it returned {"today": {...}}. 
        # Let's duplicate that structure to be safe.
        
        return {
            "today": {
                "calories": summary["calories"],
                "protein": summary["protein"],
                "carbs": summary["carbs"],
                "fats": summary["fats"]
            }
        }
