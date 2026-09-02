import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    @property
    def DATABASE_URL(self) -> str:
        # Use DATABASE_URL if provided (for cloud deployments like Neon)
        # Otherwise fall back to individual components (for local development)
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return database_url
        
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "crud")
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


settings = Settings()
