from pydantic import  RedisDsn, AmqpDsn
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

    csv_path: PathData = base_dir("csv_files")

    media_root: str = base_dir("media").file_path
    media_url: str = "media/"
    static_root: str = base_dir("static").file_path
    static_url: str = "static/"

    debug: bool = True  # bool_value
    secret_key: str = "django-insecure-key"
    allowed_hosts: str = "*"
    django_admin_url: str = 'admin/'
    logging_level: str = 'INFO'

    project_env: str = 'local'

    postgres_engine: str = 'django.contrib.gis.db.backends.postgis'
    postgres_db: str = project_name
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    postgres_host: str = 'postgres'
    postgres_port: str = ''
    postgres_atomic_requests: bool = True  # bool_value

    django_email_host_user: str = 'admin@matilda.com'
    django_email_host_password: str = 'key'

    use_docker: bool = False  # bool_value

    redis_dns: RedisDsn = 'redis://localhost:6379/0'
    rabbitmq_dns: AmqpDsn = 'amqp://localhost:5672/'
    celery_broker_url: str = rabbitmq_dns
    celery_result_backend: str = rabbitmq_dns

    ## Django Superuser credentials
    # usage:
    # source .env
    # python manage.py createsuperuser --noinput
    django_superuser_username: str = ""
    django_superuser_password: str = ""
    django_superuser_email: str = ""

config = Settings()