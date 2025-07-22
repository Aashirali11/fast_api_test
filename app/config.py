from pydantic_settings import BaseSettings
from pydantic import field_validator,model_validator
# from dotenv import load_dotenv

# # # Load .env file before reading settings
# load_dotenv()

class AppSettings(BaseSettings):
    dbname: str  # Required — raises error if missing
    dbhost: str
    dbpass: str
    dbuser: str
    postgres_port: int = 5432  # Default value if not provided
    postgres_connection_url: str = ""  # Will be built from other fields
    
    @field_validator("dbpass")
    def url_encode_pass(cls, v: str) -> str:
        from urllib.parse import quote
        return quote(v, safe='')
    
    @model_validator(mode="after")
    def build_connection_url(cls, values):
        values.postgres_connection_url = (
            f"postgresql+psycopg://{values.dbuser}:{values.dbpass}@"
            f"{values.dbhost}:{values.postgres_port}/{values.dbname}"
        )
        return values


    class Config:
        env_file = ".env"  # Optional: fallback if .env not loaded manually

# Create a single settings instance to reuse
settings = AppSettings()
# print(f'{settings.iss=}{type(settings.iss)}')