from api.v1.api_router import api_router
from core.celery_app import celery_app  # noqa: F401
from core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. Create an instance of the FastAPI class
app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix=settings.API_V1_STR)

origins = [
    settings.FRONTEND_HOST,  # Default Vite port
]
# In production, replace ["*"] with your actual domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_data():
    return {"message": "Hello from FastAPI"}
