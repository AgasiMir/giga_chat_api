from fastapi import FastAPI
from src.routers import routers

app = FastAPI(title="AI стартап", version="1.0.0")


for router in routers:
    app.include_router(router)
