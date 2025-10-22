from pydantic_settings import BaseSettings

#Environment variables
class Settings(BaseSettings): # type: ignore
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        case_sensitive = False 

settings = Settings() # type: ignore