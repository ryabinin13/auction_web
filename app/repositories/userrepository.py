from app.models import User
from app.database import SessionLocal
from app.repositories.baserepository import CRUDRepository, GetUserEmail

class UserRepository(CRUDRepository, GetUserEmail):

    def __init__(self):
        self.db = SessionLocal()

    def create(self, data: dict) -> None:
        user = User(
            username=data['username'], 
            email=data['email'], 
            password_hash=data['password_hash'], 
            birthday=data['birthday'],
            phone_number = data['phone_number']
        )

        self.db.add(user)
        self.db.commit()
        
        return None

    def get_id(self, id: int) -> User:
        return self.db.query(User).where(User.id == id).first()

    def get_email(self, email: str) -> User:
        user = self.db.query(User).where(User.email == email).first()
        return user

    def getall(self):
        return self.db.query(User).all()

    def update(self, user: User, data: dict) -> None:
        user = User(
            id = user.id,
            username=data['username'], 
            email=data['email'], 
            password_hash=data['password_hash'], 
            birthday=data['birthday'],
            phone_number = data['phone_number']
        )
        self.db.merge(user)
        self.db.commit()
        return None

    def delete(self, id: int) -> None:
        user = self.db.query(User).filter(User.id == id).delete()
        self.db.commit()
        return None


