from celery import Celery
from celery.schedules import crontab
from core.config import settings
from kombu import Exchange, Queue

# Create Celery app
celery_app = Celery(__name__, include=["tasks.task"])

# Configuration
celery_app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Define queues
celery_app.conf.task_queues = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("high_priority", Exchange("high_priority"), routing_key="high_priority"),
    Queue("low_priority", Exchange("low_priority"), routing_key="low_priority"),
)

# Default queue
celery_app.conf.task_default_queue = "default"
celery_app.conf.task_default_exchange = "default"
celery_app.conf.task_default_routing_key = "default"

# Beat schedule (periodic tasks)
celery_app.conf.beat_schedule = {
    "cleanup-every-minute": {
        "task": "tasks.task.example_task",
        "schedule": 60.0,  # Run every minute
    },
    "cleanup-every-hour": {
        "task": "tasks.task.cleanup_task",
        "schedule": crontab(minute=0),  # Run every hour
    },
    "daily-report-at-midnight": {
        "task": "tasks.task.daily_report",
        "schedule": crontab(hour=0, minute=0),  # Run at midnight UTC
    },
}


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
