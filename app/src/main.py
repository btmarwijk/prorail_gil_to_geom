from api.v1.api_router import api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. Create an instance of the FastAPI class
app = FastAPI(title="KabelLeiding GIS API")

app.include_router(api_router, prefix="/api/v1")

# In production, replace ["*"] with your actual domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/data")
async def get_data():
    return {"message": "Hello from FastAPI"}
