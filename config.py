from pydantic import BaseSettings

class Settings(BaseSettings):
    imdb_key: str
    front_url: str
    api_url: str

    class Config:
        env_file = ".env"

settings = Settings()