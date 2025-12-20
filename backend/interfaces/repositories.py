from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

class IUserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def create_user(self, user_data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        pass

class IFoodRepository(ABC):
    @abstractmethod
    def search_foods(self, query: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def add_food(self, food_data: Dict[str, Any]) -> str:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Dict[str, Any]]:
        pass

class IMealRepository(ABC):
    @abstractmethod
    def add_meal_log(self, log_data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def get_logs_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_logs_by_date_range(self, user_id: str, start_date: datetime) -> List[Dict[str, Any]]:
        pass
