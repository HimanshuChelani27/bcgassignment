from pydantic_settings import BaseSettings

from typing import Optional
from pydantic import Extra
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SENDER_EMAIL: Optional[str]
    EMAIL_APP_PASSWORD: Optional[str]
    URL:str
    ALGORITHM_JWT: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SECRET_KEY: str ='himanshuchelani'
   
    class Config:
        env_file = ".env"
        extra = Extra.allow


settings = Settings()
