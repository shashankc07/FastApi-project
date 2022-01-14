from pydantic import BaseSettings


class Settings(BaseSettings):    # class for setting up environment path variables
    db_hostname: str = "localhost"
    db_port: str = "8080"
    db_name: str
    db_username: str
    db_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
