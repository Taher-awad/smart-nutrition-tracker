from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import timedelta

class IAuthenticationService(ABC):
    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def register_user(self, user_data: Dict[str, Any], password: str) -> str:
        pass
    
    @abstractmethod
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        pass

class IUserProfileService(ABC):
    @abstractmethod
    def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def update_profile(self, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def calculate_bmr_tdee(self, data: Dict[str, Any]) -> float:
        pass

class IMealService(ABC):
    @abstractmethod
    def search_foods(self, query: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def add_custom_food(self, food_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def log_meal(self, user_id: str, meal_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_meal_history(self, user_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_daily_summary(self, user_id: str) -> Dict[str, Any]:
        pass

class IAIEngine(ABC):
    @abstractmethod
    def recognize_image(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def generate_meal_plan(self, user_id: str) -> Dict[str, Any]:
        pass
