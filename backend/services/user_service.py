from repositories.user_repository import UserRepository
from interfaces.services import IUserProfileService
from typing import Dict, Any, Optional

class UserProfileService(IUserProfileService):
    def __init__(self):
        self.user_repo = UserRepository()

    def get_profile(self, user_id: int) -> Optional[Any]:
        return self.user_repo.find_by_id(user_id)

    def update_profile(self, user_id: int, update_data: Dict[str, Any]) -> Any:
        # Calculate BMR/TDEE if relevant fields are present
        if all(k in update_data for k in ["weight", "height", "age", "gender", "activity_level", "goal"]):
            daily_calories = self.calculate_bmr_tdee(update_data)
            update_data["daily_calorie_goal"] = daily_calories
        
        return self.user_repo.update_user(user_id, update_data)

    def calculate_bmr_tdee(self, data: Dict[str, Any]) -> float:
        # Mifflin-St Jeor Equation
        weight = data.get("weight", 70)
        height = data.get("height", 170)
        age = data.get("age", 30)
        gender = data.get("gender", "male")
        activity_level = data.get("activity_level", "sedentary")
        goal = data.get("goal", "maintain")

        if gender.lower() == "male":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        tdee = bmr * activity_multipliers.get(activity_level.lower(), 1.2)
        
        if goal == "lose":
            return tdee - 500
        elif goal == "gain":
            return tdee + 500
        return tdee
