from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # MySQL Database
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "washli"
    db_ssl_ca: str = "certs/ca.pem"
    db_ssl_enabled: bool = True
    
    # Application
    secret_key: str = "change-this-secret-key"
    firebase_credentials_path: str = "serviceAccountKey.json"
    firestore_database_id: str = "merchant-onboarding"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()
