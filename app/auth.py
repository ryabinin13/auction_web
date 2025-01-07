from authx import AuthX, AuthXConfig
import os
from dotenv import load_dotenv

config = AuthXConfig()

load_dotenv()

config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "auction_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
config.JWT_ACCESS_TOKEN_EXPIRES = 300

security = AuthX(config=config)
