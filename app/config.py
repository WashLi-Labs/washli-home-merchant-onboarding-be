from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    secret_key: str = "change-this-secret-key"
    firebase_credentials_path: str = "serviceAccountKey.json"
    firestore_database_id: str = "merchant-onboarding"
    firebase_storage_bucket: str = "washli-2a77a.firebasestorage.app"

    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings():
    return Settings()
