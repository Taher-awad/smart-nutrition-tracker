from repositories.base import BaseRepository
from models import FoodItem
from typing import List
from sqlmodel import select, col

class FoodRepository(BaseRepository[FoodItem]):
    def __init__(self):
        super().__init__(FoodItem)

    def search_foods(self, query: str) -> List[FoodItem]:
        with self.get_session() as session:
            # Case-insensitive search
            statement = select(FoodItem).where(col(FoodItem.name).ilike(f"%{query}%"))
            return session.exec(statement).all()

    def add_custom_food(self, food_data: dict) -> FoodItem:
        food = FoodItem(**food_data)
        food.is_custom = True
        return self.insert_one(food)
