from typing import List, Optional, Type, TypeVar, Generic
from sqlmodel import Session, select, SQLModel
from database import get_session

T = TypeVar("T", bound=SQLModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get_session(self) -> Session:
        # In a real app with dependency injection, we might pass the session in __init__
        # For simplicity in this migration, we'll create a new session per operation
        # or use a context manager. Ideally, FastAPI dependency injection handles this.
        # However, to keep the repository pattern similar to before without passing session everywhere:
        return next(get_session())

    def find_one(self, **kwargs) -> Optional[T]:
        with self.get_session() as session:
            statement = select(self.model).filter_by(**kwargs)
            return session.exec(statement).first()

    def find_all(self, **kwargs) -> List[T]:
        with self.get_session() as session:
            statement = select(self.model).filter_by(**kwargs)
            return session.exec(statement).all()

    def insert_one(self, data: T) -> T:
        with self.get_session() as session:
            session.add(data)
            session.commit()
            session.refresh(data)
            return data

    def update_one(self, id: int, update_data: dict) -> Optional[T]:
        with self.get_session() as session:
            db_item = session.get(self.model, id)
            if not db_item:
                return None
            
            for key, value in update_data.items():
                setattr(db_item, key, value)
            
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item

    def delete_one(self, id: int) -> bool:
        with self.get_session() as session:
            db_item = session.get(self.model, id)
            if not db_item:
                return False
            session.delete(db_item)
            session.commit()
            return True
            
    def find_by_id(self, id: int) -> Optional[T]:
        with self.get_session() as session:
            return session.get(self.model, id)
