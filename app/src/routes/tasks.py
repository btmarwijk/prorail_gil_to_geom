from celery.result import AsyncResult
from core.celery_app import celery_app
from fastapi import APIRouter
from pydantic import BaseModel
from tasks.task import example_task, long_running_task

router = APIRouter()


class TaskData(BaseModel):
    data: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: dict = None


@router.post("/trigger-example")
async def trigger_example_task():
    """
    Trigger the example task and return task ID for tracking.
    """
    task = example_task.delay()
    return {"task_id": task.id, "message": "Task triggered"}


@router.post("/trigger-long-running")
async def trigger_long_running(body: TaskData):
    """
    Trigger a long-running task with data.
    """
    task = long_running_task.delay(body.data)
    return {"task_id": task.id, "message": "Long-running task triggered"}


@router.get("/status/{task_id}")
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """
    Get the status of a task by its ID.
    """
    result = AsyncResult(task_id, app=celery_app)

    if result.state == "PENDING":
        return TaskStatusResponse(
            task_id=task_id,
            status="PENDING",
            result={"message": "Task not found or not started"},
        )
    elif result.state == "STARTED":
        return TaskStatusResponse(
            task_id=task_id, status="STARTED", result={"message": "Task is running"}
        )
    elif result.state == "RETRY":
        return TaskStatusResponse(
            task_id=task_id, status="RETRY", result={"message": "Task is being retried"}
        )
    elif result.state == "FAILURE":
        return TaskStatusResponse(
            task_id=task_id, status="FAILURE", result={"error": str(result.info)}
        )
    elif result.state == "SUCCESS":
        return TaskStatusResponse(
            task_id=task_id, status="SUCCESS", result=result.result
        )
    else:
        return TaskStatusResponse(
            task_id=task_id, status=result.state, result=result.result
        )


@router.delete("/revoke/{task_id}")
async def revoke_task(task_id: str):
    """
    Cancel/revoke a task.
    """
    AsyncResult(task_id, app=celery_app).revoke(terminate=True)
    return {"message": f"Task {task_id} revoked"}


@router.get("/health")
async def task_queue_health():
    """
    Check Celery/Redis health.
    """
    try:
        # Simple ping to check broker connection
        inspect = celery_app.control.inspect()
        stats = inspect.stats()

        if stats:
            return {
                "status": "healthy",
                "workers": len(stats),
                "message": "Task queue is operational",
            }
        else:
            return {
                "status": "degraded",
                "workers": 0,
                "message": "No workers connected to broker",
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "Unable to connect to task queue",
        }
