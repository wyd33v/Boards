from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from models.base import DBase

T = TypeVar("T", bound=DBase)


class Repository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def save(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: T) -> None:
        self.db.delete(obj)
        self.db.commit()

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def get_by_id(self, pk: int) -> Optional[T]:
        return self.db.query(self.model).get(pk)

    def get_by_param(self, **filters) -> Optional[T]:
        return self.db.query(self.model).filter_by(**filters).one_or_none()
