from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
	app_name: str = "LabTracker"
	db_host: str
	db_port: int
	db_name: str
	db_user: str
	db_pass: str
	secret: str

	class Config:
		env_file = ".env"


@lru_cache()
def get_settings():
	return Settings()


settings = get_settings()
