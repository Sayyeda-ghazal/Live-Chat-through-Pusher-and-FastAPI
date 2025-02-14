from pydantic_settings import BaseSettings



class Settings(BaseSettings):

    DATABASE_URL: str = 'postgresql://postgres:ghazaldb1@localhost:5432/messages'




def get_settings() -> Settings:
    return Settings()