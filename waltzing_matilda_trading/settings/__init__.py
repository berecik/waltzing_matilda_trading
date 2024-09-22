from split_settings.tools import optional, include
from config import config

include(
    "base.py",
    "django_extensions.py",
    "db.py",
    "local_apps.py",
    "celery.py",
    "healthz.py",
    "logging.py",
    "jwt.py",
    optional(f"envs/{config.project_env}.py"),
)
