import time

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3)
def example_task(self):
    """
    Example task that demonstrates basic Celery functionality.
    """
    try:
        logger.info("Starting example_task")
        # Your business logic here
        time.sleep(2)
        logger.info("example_task completed")
        return {"status": "success", "message": "Example task completed"}
    except Exception as exc:
        logger.error(f"Task failed: {exc}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2**self.request.retries))


@shared_task(bind=True)
def cleanup_task(self):
    """
    Periodic task to clean up old data (runs hourly).
    """
    try:
        logger.info("Starting cleanup_task")
        # Add your cleanup logic here
        logger.info("cleanup_task completed")
        return {"status": "success", "message": "Cleanup completed"}
    except Exception as exc:
        logger.error(f"Cleanup failed: {exc}")
        return {"status": "error", "message": str(exc)}


@shared_task(bind=True)
def daily_report(self):
    """
    Periodic task to generate daily reports (runs daily at midnight UTC).
    """
    try:
        logger.info("Generating daily report")
        # Add your report generation logic here
        logger.info("Daily report generated")
        return {"status": "success", "message": "Daily report generated"}
    except Exception as exc:
        logger.error(f"Report generation failed: {exc}")
        return {"status": "error", "message": str(exc)}


@shared_task(bind=True, max_retries=3)
def long_running_task(self, task_data):
    """
    Example long-running task with parameters.
    """
    try:
        logger.info(f"Starting long_running_task with data: {task_data}")
        # Simulate long-running operation
        for i in range(10):
            logger.info(f"Progress: {i + 1}/10")
            time.sleep(1)
        logger.info("long_running_task completed")
        return {"status": "success", "result": task_data}
    except Exception as exc:
        logger.error(f"Task failed: {exc}")
        raise self.retry(exc=exc, countdown=60 * (2**self.request.retries))
