from pydantic import  RedisDsn
from pydantic_settings import BaseSettings
from beret_utils import PathData

PROJECT_NAME = "waltzing_matilda_trading"

base_dir = PathData.main()
home_dir = PathData.home()
settings_dir = base_dir(PROJECT_NAME)


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    project_name: str = PROJECT_NAME
    redis_dns: RedisDsn = "redis://localhost:6379/0"
    media_root: str = "media"
    static_root: str = "static"
    debug: bool = True  # bool_value
    project_env: str = 'local'
    postgres_engine: str = 'django.contrib.gis.db.backends.postgis'
    postgres_db: str = PROJECT_NAME
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    postgres_host: str = 'postgres'
    postgres_port: str = ''
    postgres_atomic_requests: bool = True  # bool_value
    secret_key: str = "django-insecure-key"
    django_email_host_user: str = 'admin@matilda.com'
    django_email_host_password: str = 'key'
    use_docker: bool = False  # bool_value
    allowed_hosts: str = "*"
    django_admin_url: str = 'admin/'
    logging_level: str = 'INFO'

config = Settings()