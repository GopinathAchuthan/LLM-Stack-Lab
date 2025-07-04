from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_username: str
    db_password: str 
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")


settings = Settings()