from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"
        
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int

    FRONTEND_URL: str

settings = Settings()