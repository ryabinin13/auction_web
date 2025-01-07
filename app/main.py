from fastapi import FastAPI
from app.routers.users import user_router
from app.routers.home import home_router
from app.database import Base, engine
import uvicorn

app = FastAPI()

app.include_router(user_router)
app.include_router(home_router)

Base.metadata.create_all(engine)

if __name__ == "__main__":
       uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)