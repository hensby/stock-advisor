from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./data/stock_advisor.db"
    redis_url: str = "redis://localhost:6379/0"
    finnhub_api_key: str = ""
    youtube_api_key: str = ""
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    default_weight_technical: float = 0.40
    default_weight_institutional: float = 0.30
    default_weight_youtube: float = 0.20
    default_weight_fundamental: float = 0.10

    stock_universe: str = "sp500"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()
