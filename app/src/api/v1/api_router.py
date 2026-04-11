from api.v1.endpoints.upload_view import router
from fastapi import APIRouter

api_router = APIRouter()

# Include the router from the upload module
api_router.include_router(router, prefix="/uploads", tags=["Uploads"])
