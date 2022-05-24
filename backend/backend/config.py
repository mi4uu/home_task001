import os


APP_PORT = os.environ.get("APP_PORT", "8000")
APP_HOST = os.environ.get("APP_HOST", " 0.0.0.0")
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://user:password@postgresserver/db"
)
CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_URL", "postgresql://user:password@postgresserver/db"
)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "postgresql://user:password@postgresserver/db"
)
