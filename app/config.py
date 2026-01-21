from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # MySQL Database
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "merchant_onboarding"
    db_ssl_ca: str = "certs/ca.pem"
    db_ssl_enabled: bool = True
    
    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    from_email: str = "noreply@yourcompany.com"
    
    # Application
    secret_key: str = "change-this-secret-key"
    otp_expiry_minutes: int = 5
    upload_dir: str = "uploads"
    
    # Google Maps
    google_maps_api_key: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()
