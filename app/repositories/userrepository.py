from app.models import User
from app.database import get_session
from app.repositories.baserepository import CRUDRepository, GetUserEmail

class UserRepository(CRUDRepository, GetUserEmail):

    def create(self, data: dict) -> None:
        with get_session() as db:
            user = User(
                username=data['username'], 
                email=data['email'], 
                password_hash=data['password_hash'], 
                birthday=data['birthday'],
                phone_number = data['phone_number']
            )

            db.add(user)
            db.commit()
            
            return None

    def get_id(self, id: int) -> User:
        with get_session() as db:
            return db.query(User).where(User.id == id).first()

    def get_email(self, email: str) -> User:
        with get_session() as db:
            user = db.query(User).where(User.email == email).first()
            return user

    def getall(self):
        with get_session() as db:
            return db.query(User).all()

    def update(self, user: User, data: dict) -> None:
        with get_session() as db:
            user = User(
                id = user.id,
                username=data['username'], 
                email=data['email'], 
                password_hash=data['password_hash'], 
                birthday=data['birthday'],
                phone_number = data['phone_number']
            )
            db.merge(user)
            db.commit()
            return None

    def delete(self, id: int) -> None:
        with get_session() as db:
            db = db
            user = db.query(User).filter(User.id == id).delete()
            db.commit()
            return None


