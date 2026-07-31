from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    # App settings
    app_name: str = "Real-Time Phishing Website Detection and Prevention"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"
    debug: bool = True


    # Database
    mongo_uri: str = "mongodb://localhost:27017"
    database_name: str = "phishing_detection"
# add this
    mongo_database: str = "phishing_detection"

    # Detection
    phishing_threshold: float = 0.75
    suspicious_threshold: float = 0.45


    # CORS
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    allowed_origin_regex: str | None = None


    class Config:
        env_file = ".env"
        case_sensitive = False



@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()