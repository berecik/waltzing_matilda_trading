from .base import MIDDLEWARE

MIDDLEWARE.append("utils.healthz.HealthCheckMiddleware")
HEALTH = True
