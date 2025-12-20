from repositories.food_repository import FoodRepository
from interfaces.services import IAIEngine
from typing import List, Dict, Any
import random
from datetime import datetime, timedelta

class AIEngine(IAIEngine):
    def __init__(self):
        self.food_repo = FoodRepository()

    def recognize_image(self) -> Dict[str, Any]:
        # Mock AI: Returns a random food from DB or a fixed one
        foods = self.food_repo.find_all()
        if foods:
            recognized = random.choice(foods)
            # recognized is a FoodItem object
            # API expects a dict or object. Returning dict for safety if response model expects it, 
            # but response model is FoodItem, so object is fine.
            return recognized
        return {"name": "Unknown Food", "calories": 0, "protein": 0, "carbs": 0, "fats": 0}

    def generate_meal_plan(self, user_id: int) -> Dict[str, Any]:
        # Mock Planner: Generates a random plan for 7 days
        start_date = datetime.utcnow()
        meals = []
        foods = self.food_repo.find_all()
        
        if not foods:
            foods = [{"name": "Apple", "calories": 95, "protein": 0.5, "carbs": 25, "fats": 0.3}]
        # If foods contains objects, we need to handle them. 
        # If empty, we made a list of dicts. Mixed types risks errors.
        # Let's ensure 'foods' is a list of dicts for the logic below, or handle objects.
        
        food_list = []
        for f in foods:
             if isinstance(f, dict):
                 food_list.append(f)
             else:
                 food_list.append(f.dict())
        
        for i in range(7):
            day_date = start_date + timedelta(days=i)
            for meal_type in ["breakfast", "lunch", "dinner"]:
                food = random.choice(food_list)
                food_copy = food.copy()
                if "id" in food_copy:
                    del food_copy["id"]
                if "_id" in food_copy: # Legacy cleanup
                    del food_copy["_id"]
                
                meals.append({
                    "date": day_date.isoformat(),
                    "meal_type": meal_type,
                    "food": food_copy
                })
                
        return {
            "user_id": user_id,
            "start_date": start_date,
            "meals": meals
        }

    def generate_meal_plan_variations(self, user_id: int) -> List[Dict[str, Any]]:
        variations = []
        
        # 10 Presets
        presets = [
            {"name": "Muscle Gain", "desc": "High protein meals to support muscle growth.", "bias": "protein"},
            {"name": "Weight Loss", "desc": "Calorie-conscious meals for steady weight loss.", "bias": "low_cal"},
            {"name": "Keto", "desc": "Low carb, high fat diet.", "bias": "keto"},
            {"name": "Paleo", "desc": "Whole foods, no processed grains.", "bias": "paleo"},
            {"name": "Vegan", "desc": "Plant-based power.", "bias": "vegan"},
            {"name": "Vegetarian", "desc": "Meat-free balanced diet.", "bias": "veg"},
            {"name": "Balanced", "desc": "A mix of all macronutrients.", "bias": "balanced"},
            {"name": "Low Carb", "desc": "Reduced carbohydrates.", "bias": "low_carb"},
            {"name": "High Energy", "desc": "Complex carbs for sustained energy.", "bias": "energy"},
            {"name": "Budget Friendly", "desc": "Cost-effective nutritious meals.", "bias": "budget"},
        ]
        
        start_date = datetime.utcnow()
        all_foods = self.food_repo.find_all()
        # Normalize to list of dicts
        food_list = []
        for f in all_foods:
             if isinstance(f, dict): food_list.append(f)
             else: food_list.append(f.dict())
             
        if not food_list:
            food_list = [{"name": "Generic Food", "calories": 100, "protein": 5, "carbs": 10, "fats": 2, "is_custom": False}]

        for preset in presets:
            meals = []
            # Filtering logic (Mocked for now as we don't have tags in DB yet)
            # In a real app, we'd filter food_list based on preset['bias']
            
            # Create a 3-day plan for brevity (or 7)
            for i in range(3): 
                day_date = start_date + timedelta(days=i)
                for meal_type in ["breakfast", "lunch", "dinner"]:
                    # Randomized selection for variety
                    food = random.choice(food_list)
                    food_copy = food.copy()
                    if "id" in food_copy: del food_copy["id"]
                    if "_id" in food_copy: del food_copy["_id"]
                    
                    meals.append({
                        "date": day_date.isoformat(),
                        "meal_type": meal_type,
                        "food": food_copy
                    })
            
            grocery_list = self._generate_grocery_list(meals)
            
            variations.append({
                "goal_name": preset["name"],
                "description": preset["desc"],
                "meals": meals,
                "grocery_list": grocery_list
            })
            
        return variations

    def _generate_grocery_list(self, meals: List[Dict]) -> List[str]:
        # Simple aggregation
        counts = {}
        for m in meals:
            name = m["food"]["name"]
            counts[name] = counts.get(name, 0) + 1
            
        g_list = []
        for name, count in counts.items():
            g_list.append(f"{count}x {name}")
        return g_list
