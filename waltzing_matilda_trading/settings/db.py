from config import config
from .base import DATABASES

DATABASES["default"] = {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        'ENGINE':   config.postgres_engine,
        'NAME':     config.postgres_db,
        'USER':     config.postgres_user,
        'PASSWORD': config.postgres_password,
        'HOST':     config.postgres_host,
        'PORT':     config.postgres_port,
        'ATOMIC_REQUESTS':  config.postgres_atomic_requests
}