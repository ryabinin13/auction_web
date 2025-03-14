from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class CRUDRepository(ABC):

    @abstractmethod
    def create(self, data: dict):
        pass

    @abstractmethod
    def get_id(self, id: int):
        pass

    @abstractmethod
    def getall(self):
        pass

    @abstractmethod
    def update(self, id: int, data: dict):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

