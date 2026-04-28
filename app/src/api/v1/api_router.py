from api.v1.endpoints.upload_view import router
from fastapi import APIRouter
from routes.tasks import router as tasks_router

api_router = APIRouter()

# Include the router from the upload module
api_router.include_router(router, prefix="/uploads", tags=["uploads"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
