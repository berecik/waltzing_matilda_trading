from split_settings.tools import optional, include
from config import config
include(
    'base.py',
    'db.py',
    'local_apps.py',
    'celery.py',
    'healthz.py',
    'logging.py',
    # optional(f'project_envs/{config.PROJECT_ENV}.py')
)
