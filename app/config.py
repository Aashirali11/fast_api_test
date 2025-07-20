from pydantic_settings import BaseSettings
from pydantic import field_validator
# from dotenv import load_dotenv

# # # Load .env file before reading settings
# load_dotenv()

class AppSettings(BaseSettings):
    dbname: str  # Required — raises error if missing
    dbhost: str
    dbpass: str
    dbuser: str

    @field_validator("dbpass")
    def url_encode_pass(cls, v: str) -> str:
        from urllib.parse import quote
        return quote(v, safe='')
    
    class Config:
        env_file = ".env"  # Optional: fallback if .env not loaded manually

# Create a single settings instance to reuse
settings = AppSettings()
# print(f'{settings.iss=}{type(settings.iss)}')