from .base import MIDDLEWARE
# from utils.healthz import HealthCheckMiddleware

MIDDLEWARE.append("utils.healthz.HealthCheckMiddleware")