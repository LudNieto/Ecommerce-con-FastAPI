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

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    FRONTEND_URL: str


settings = Settings()
